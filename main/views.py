from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect

from .models import Diff
from .models import Score
from .forms import ScoreForm

from django.views.generic import ListView
from django.views.generic import UpdateView


import math
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from urllib.parse import unquote




#create function
def make_rate(score, const):
    score = int(score)
    const = float(const)
    if score == 1010000:
        rate = const+3.7
    elif score >= 1008000:
        rate = const+3.4+(score-1008000)/10000
    elif score >= 1004000:
        rate = const+2.4+(score-1004000)/4000
    elif score >= 1000000:
        rate = const+2+(score-1000000)/10000
    elif score >= 980000:
        rate = const+1+(score-980000)/20000
    elif score >= 950000:
        rate = const+(score-950000)/30000
    elif score >= 900000:
        rate = const-1+(score-900000)/50000
    elif score >= 500000:
        rate = const-5+(score-500000)/100000
    else:
        rate=0
    return float(rate)

def cul_op(score, const, fc, ap):
    if score == 1010000:
        return float((const+3)*5)
    elif score >= 1008000:
        if ap == True:
            return float((const+2)*5+1+(score-1008000)*0.001875)
        elif fc == True:
            return float((const+2)*5+0.5+(score-1008000)*0.001875)
        else:
            return float((const+2)*5+(score-1008000)*0.001875)
    elif score >= 950000:
        if ap == True:
            return float(const*5+1)
        elif fc == True:
            return float(const*5+0.5)
        else:
            return float(const*5)
    else:
        return 0

def search_diff(const):
    if float(const) <= 10.5:
        return float(int(const))
    elif float(const) - int(const) <= 0.5:
        return float(int(const))
    elif float(const) - int(const) > 0.5:
        return float(int(const))+0.5



# Create your views here.
class LookingBest(ListView):
    model = Diff
    template_name = "main/best.html"
    context_object_name = "best_forty"

    def get_queryset(self):
        raw_query = """
            SELECT s.id, s.title, s.I_score, s.II_score, s.III_score, s.IV_score, s.IV_a_score, d.I_diff, d.II_diff, d.III_diff, d.IV_diff, d.IV_a_diff
            FROM main_Score AS s
            LEFT JOIN main_Diff AS d
            ON s.title = d.title
        """
        raw_records = list(Score.objects.raw(raw_query))

        #処理
        made_I_rate = [(record.title, round(make_rate(record.I_score, record.I_diff), 5), "I", record.I_diff, record.I_score) if record.I_score is not None else (record.title, None, "I", record.I_diff, record.I_score) for record in raw_records]
        made_II_rate = [(record.title, round(make_rate(record.II_score, record.II_diff), 5), "II", record.II_diff, record.II_score) if record.II_score is not None else (record.title, None, "II", record.II_diff, record.II_score) for record in raw_records]
        made_III_rate = [(record.title, round(make_rate(record.III_score, record.III_diff), 5), "III", record.III_diff, record.III_score) if record.III_score is not None else (record.title, None, "III", record.III_diff, record.III_score) for record in raw_records]
        made_IV_rate = [(record.title, round(make_rate(record.IV_score, record.IV_diff), 5), "IV", record.IV_diff, record.IV_score) if record.IV_score is not None else (record.title, None, "IV", record.IV_diff, record.IV_score) for record in raw_records]
        made_IV_a_rate = [(record.title, round(make_rate(record.IV_a_score, record.IV_a_diff), 5) if record.IV_a_score is not None else None, "IV_a", record.IV_a_diff, record.IV_a_score) for record in raw_records if record.IV_a_diff is not None]


        rate_table = made_I_rate + made_II_rate + made_III_rate + made_IV_rate + made_IV_a_rate

        rate_table = sorted(rate_table, key=lambda x: (
        x[1] is None,
        x[1] if x[1] is not None else -float('inf'),
        x[3],
        ), reverse=True)

        best_table = [item for item in rate_table if item[1] is not None]

        ten_rate = 0
        ten_rate_count = 0
        for a in best_table[:10] :
            ten_rate+=float(a[1])
            ten_rate_count += 1
        
        thirty_rate = 0
        thirty_rate_count = 0
        for a in best_table[10:40] :
            thirty_rate+=float(a[1])
            thirty_rate_count += 1

        middle_rate = 0
        middle_rate_count = 0
        for a in best_table[10:20] :
            middle_rate+=float(a[1])
            middle_rate_count += 1

        bottom_rate = 0
        bottom_rate_count = 0
        for a in best_table[20:40] :
            bottom_rate+=float(a[1])
            bottom_rate_count += 1


        rate=0
        if bottom_rate_count !=0 :
            rate=(ten_rate/10)*0.6+(middle_rate/10)*0.2+(bottom_rate/bottom_rate_count)*0.2
        else:
            if middle_rate_count !=0 :
                rate=(ten_rate/10)*0.6+(middle_rate/middle_rate_count)*0.2
            elif ten_rate_count !=0:
                rate=(ten_rate/ten_rate_count)*0.6
            else:
                rate=0

        real_rate = math.floor(rate * 10**3) / 10**3
            


        if ten_rate_count != 0:
            if thirty_rate_count != 0:
                return [best_table[:40], ten_rate/ten_rate_count, thirty_rate/thirty_rate_count, rate, best_table[:40][-1:], real_rate, self.request.user]
            else:
                return [best_table[:40], ten_rate/ten_rate_count, 0, rate, best_table[:40][-1:], real_rate, self.request.user]
        else:
            return [best_table[:40], 0, 0, rate, best_table[-1:], real_rate, self.request.user]


        
class LookingRecords(ListView):
    model = Score
    template_name = "main/records.html"
    context_object_name = "list"

    def get_queryset(self):
        raw_query = """
            SELECT s.id, s.title, s.I_score, s.II_score, s.III_score, s.IV_score, s.IV_a_score, d.I_diff, d.II_diff, d.III_diff, d.IV_diff, d.IV_a_diff, s.I_clear, s.II_clear, s.III_clear, s.IV_clear, s.IV_a_clear, s.I_fc, s.II_fc, s.III_fc, s.IV_fc, s.IV_a_fc, s.I_ap, s.II_ap, s.III_ap, s.IV_ap, s.IV_a_ap
            FROM main_Score AS s
            LEFT JOIN main_Diff AS d
            ON s.title = d.title
        """

        raw_records = list(Score.objects.raw(raw_query))

        songs_list = [(record.title, (record.I_diff, record.I_score, record.I_clear, record.I_fc, record.I_ap), (record.II_diff, record.II_score, record.II_clear, record.II_fc, record.II_ap), (record.III_diff, record.III_score, record.III_clear, record.III_fc, record.III_ap), (record.IV_diff, record.IV_score, record.IV_clear, record.IV_fc, record.IV_ap), (record.IV_a_diff, record.IV_a_score, record.IV_a_clear, record.IV_a_fc, record.IV_a_ap), record.id) if record.IV_a_diff is not None else (record.title, (record.I_diff, record.I_score, record.I_clear, record.I_fc, record.I_ap), (record.II_diff, record.II_score, record.II_clear, record.II_fc, record.II_ap), (record.III_diff, record.III_score, record.III_clear, record.III_fc, record.III_ap), (record.IV_diff, record.IV_score, record.IV_clear, record.IV_fc, record.IV_ap), record.id) for record in raw_records]

        songs_list = sorted(songs_list, key=lambda x: x[4][0], reverse=True)

        each_list = []
        for g in songs_list:
            if g[1][1] != None:
                if g[1][4] == True:
                    each_list += [[g[0], "I", g[1][0], g[1][1], make_rate(g[1][1], g[1][0]), "ap"]]
                elif g[1][3] == True:
                    each_list += [[g[0], "I", g[1][0], g[1][1], make_rate(g[1][1], g[1][0]), "fc"]]
                elif g[1][2] == True:
                    each_list += [[g[0], "I", g[1][0], g[1][1], make_rate(g[1][1], g[1][0]), "clear"]]
                else:
                    each_list += [[g[0], "I", g[1][0], g[1][1], make_rate(g[1][1], g[1][0]), "none"]]
            
            if g[2][1] != None:
                if g[2][4] == True:
                    each_list += [[g[0], "II", g[2][0], g[2][1], make_rate(g[2][1], g[2][0]), "ap"]]
                elif g[2][3] == True:
                    each_list += [[g[0], "II", g[2][0], g[2][1], make_rate(g[2][1], g[2][0]), "fc"]]
                elif g[2][2] == True:
                    each_list += [[g[0], "II", g[2][0], g[2][1], make_rate(g[2][1], g[2][0]), "clear"]]
                else:
                    each_list += [[g[0], "II", g[2][0], g[2][1], make_rate(g[2][1], g[2][0]), "none"]]

            if g[3][1] != None:
                if g[3][4] == True:
                    each_list += [[g[0], "III", g[3][0], g[3][1], make_rate(g[3][1], g[3][0]), "ap"]]
                elif g[3][3] == True:
                    each_list += [[g[0], "III", g[3][0], g[3][1], make_rate(g[3][1], g[3][0]), "fc"]]
                elif g[3][2] == True:
                    each_list += [[g[0], "III", g[3][0], g[3][1], make_rate(g[3][1], g[3][0]), "clear"]]
                else:
                    each_list += [[g[0], "III", g[3][0], g[3][1], make_rate(g[3][1], g[3][0]), "none"]]

            if g[4][1] != None:
                if g[4][4] == True:
                    each_list += [[g[0], "IV", g[4][0], g[4][1], make_rate(g[4][1], g[4][0]), "ap"]]
                elif g[4][3] == True:
                    each_list += [[g[0], "IV", g[4][0], g[4][1], make_rate(g[4][1], g[4][0]), "fc"]]
                elif g[4][2] == True:
                    each_list += [[g[0], "IV", g[4][0], g[4][1], make_rate(g[4][1], g[4][0]), "clear"]]
                else:
                    each_list += [[g[0], "IV", g[4][0], g[4][1], make_rate(g[4][1], g[4][0]), "none"]]
            
            if len(g) > 6 :
                if g[5][1] != None:
                    if g[5][4] == True:
                        each_list += [[g[0], "IV-α", g[5][0], g[5][1], make_rate(g[5][1], g[5][0]), "ap"]]
                    elif g[5][3] == True:
                        each_list += [[g[0], "IV-α", g[5][0], g[5][1], make_rate(g[5][1], g[5][0]), "fc"]]
                    elif g[5][2] == True:
                        each_list += [[g[0], "IV-α", g[5][0], g[5][1], make_rate(g[5][1], g[5][0]), "clear"]]
                    else:
                        each_list += [[g[0], "IV-α", g[5][0], g[5][1], make_rate(g[5][1], g[5][0]), "none"]]
        
        each_list = sorted(each_list, key=lambda x: x[4], reverse=True)
            


        songs_count=0

        I_clear_count=0
        I_fc_count=0
        I_ap_count=0
        I_max_count=0
        I_sum_score=0
        I_sum_op=0
        I_max_op=0

        II_clear_count=0
        II_fc_count=0
        II_ap_count=0
        II_max_count=0
        II_sum_score=0
        II_sum_op=0
        II_max_op=0

        III_clear_count=0
        III_fc_count=0
        III_ap_count=0
        III_max_count=0
        III_sum_score=0
        III_sum_op=0
        III_max_op=0

        IV_clear_count=0
        IV_fc_count=0
        IV_ap_count=0
        IV_max_count=0
        IV_sum_score=0
        IV_sum_op=0
        IV_max_op=0

        IV_a_songs_count=0
        IV_a_clear_count=0
        IV_a_fc_count=0
        IV_a_ap_count=0
        IV_a_max_count=0
        IV_a_sum_score=0
        IV_a_sum_op=0
        IV_a_max_op=0
        for i in songs_list:
            songs_count+=1
            if i[1][2] == True:
                I_clear_count += 1
            if i[1][3] == True:
                I_fc_count += 1
            if i[1][4] == True:
                I_ap_count += 1
            if i[1][1] == 1010000:
                I_max_count += 1
            if i[1][1] is not None:
                I_sum_score += i[1][1]
                I_sum_op += cul_op(float(i[1][1]), float(i[1][0]), i[1][3], i[1][4])
            I_max_op += (float(i[1][0])+3)*5

            if i[2][2] == True:
                II_clear_count += 1
            if i[2][3] == True:
                II_fc_count += 1
            if i[2][4] == True:
                II_ap_count += 1
            if i[2][1] == 1010000:
                II_max_count += 1
            if i[2][1] is not None:
                II_sum_score += i[2][1]
                II_sum_op += cul_op(float(i[2][1]), float(i[2][0]), i[2][3], i[2][4])
            II_max_op += (float(i[2][0])+3)*5

            if i[3][2] == True:
                III_clear_count += 1
            if i[3][3] == True:
                III_fc_count += 1
            if i[3][4] == True:
                III_ap_count += 1
            if i[3][1] == 1010000:
                III_max_count += 1
            if i[3][1] is not None:
                III_sum_score += i[3][1]
                III_sum_op += cul_op(float(i[3][1]), float(i[3][0]), i[3][3], i[3][4])
            III_max_op += (float(i[3][0])+3)*5

            if i[4][2] == True:
                IV_clear_count += 1
            if i[4][3] == True:
                IV_fc_count += 1
            if i[4][4] == True:
                IV_ap_count += 1
            if i[4][1] == 1010000:
                IV_max_count += 1
            if i[4][1] is not None:
                IV_sum_score += i[4][1]
                IV_sum_op += cul_op(float(i[4][1]), float(i[4][0]), i[4][3], i[4][4])
            IV_max_op += (float(i[4][0])+3)*5

            if len(i) > 6 :
                IV_a_songs_count += 1
                if i[5][2] == True:
                    IV_a_clear_count += 1
                if i[5][3] == True:
                    IV_a_fc_count += 1
                if i[5][4] == True:
                    IV_a_ap_count += 1
                if i[5][1] == 1010000:
                    IV_a_max_count += 1
                if i[5][1] is not None:
                    IV_a_sum_score += i[5][1]
                    IV_a_sum_op += cul_op(float(i[5][1]), float(i[5][0]), i[5][3], i[5][4])
                IV_a_max_op += (float(i[5][0])+3)*5

                
        page_number = self.request.GET.get('page', 1)
        order = self.request.GET.get('order', 1)
        filter_diff = self.request.GET.get('diff', 1)
        type = self.request.GET.get('type', 1)

        priority_map = {
            'IV-α': 5,
            'IV': 4,
            'III': 3,
            'II': 2,
            'I': 1
        }


        if type == "rate":
            if order == "desc":
                each_list = sorted(each_list, key=lambda x: x[4])
            else:
                each_list = sorted(each_list, key=lambda x: x[4], reverse=True)
        elif type == "const":
            if order == "desc":
                each_list = sorted(each_list, key=lambda x: x[2])
            else:
                each_list = sorted(each_list, key=lambda x: x[2], reverse=True)
        elif type == "score":
            if order == "desc":
                each_list = sorted(each_list, key=lambda x: x[3])
            else:
                each_list = sorted(each_list, key=lambda x: x[3], reverse=True)
        elif type == "level":
            if order == "desc":
                each_list = sorted(each_list, key=lambda x: search_diff(x[2]))
            else:
                each_list = sorted(each_list, key=lambda x: search_diff(x[2]), reverse=True)
        elif type == "diff":
            if order == "desc":
                each_list = sorted(each_list, key=lambda x: priority_map.get(x[1]))
            else:
                each_list = sorted(each_list, key=lambda x: priority_map.get(x[1]), reverse=True)

        if filter_diff == "I":
            each_list = list(filter(lambda x: x[1] == filter_diff, each_list))
        elif filter_diff == "II":
            each_list = list(filter(lambda x: x[1] == filter_diff, each_list))
        elif filter_diff == "III":
            each_list = list(filter(lambda x: x[1] == filter_diff, each_list))
        elif filter_diff == "IV":
            each_list = list(filter(lambda x: x[1] == filter_diff, each_list))
        elif filter_diff == "IV-α":
            each_list = list(filter(lambda x: x[1] == filter_diff, each_list))


        each_list = Paginator(each_list, 50)

        return [each_list.get_page(page_number), songs_count, IV_a_songs_count, [I_clear_count, I_fc_count, I_ap_count, I_max_count, I_sum_score/songs_count, (I_sum_op/I_max_op)*100], [II_clear_count, II_fc_count, II_ap_count, II_max_count, II_sum_score/songs_count, (II_sum_op/II_max_op)*100], [III_clear_count, III_fc_count, III_ap_count, III_max_count, III_sum_score/songs_count, (III_sum_op/III_max_op)*100], [IV_clear_count, IV_fc_count, IV_ap_count, IV_max_count, IV_sum_score/songs_count, (IV_sum_op/IV_max_op)*100], [IV_a_clear_count, IV_a_fc_count, IV_a_ap_count, IV_a_max_count, IV_a_sum_score/IV_a_songs_count, (IV_a_sum_op/IV_a_max_op)*100], self.request.user]






class InputScore(ListView):
    model = Diff
    template_name = "main/input_score/I.html"
    context_object_name = "list"

    def get_queryset(self):
        raw_query = """
            SELECT s.id, s.title, s.I_score, s.II_score, s.III_score, s.IV_score, s.IV_a_score, d.I_diff, d.II_diff, d.III_diff, d.IV_diff, d.IV_a_diff, s.I_clear, s.II_clear, s.III_clear, s.IV_clear, s.IV_a_clear, s.I_fc, s.II_fc, s.III_fc, s.IV_fc, s.IV_a_fc, s.I_ap, s.II_ap, s.III_ap, s.IV_ap, s.IV_a_ap
            FROM main_Score AS s
            LEFT JOIN main_Diff AS d
            ON s.title = d.title
        """

        raw_records = list(Score.objects.raw(raw_query))

        songs_list = [(record.title, (record.I_diff, record.I_score, record.I_clear, record.I_fc, record.I_ap), (record.II_diff, record.II_score, record.II_clear, record.II_fc, record.II_ap), (record.III_diff, record.III_score, record.III_clear, record.III_fc, record.III_ap), (record.IV_diff, record.IV_score, record.IV_clear, record.IV_fc, record.IV_ap), (record.IV_a_diff, record.IV_a_score, record.IV_a_clear, record.IV_a_fc, record.IV_a_ap), record.id) if record.IV_a_diff is not None else (record.title, (record.I_diff, record.I_score, record.I_clear, record.I_fc, record.I_ap), (record.II_diff, record.II_score, record.II_clear, record.II_fc, record.II_ap), (record.III_diff, record.III_score, record.III_clear, record.III_fc, record.III_ap), (record.IV_diff, record.IV_score, record.IV_clear, record.IV_fc, record.IV_ap), record.id) for record in raw_records]

        songs_list = sorted(songs_list, key=lambda x: x[4][0], reverse=True)

        return [songs_list, self.request.user]

class UpdateScore(UpdateView):
    model = Score
    form_class = ScoreForm
    template_name = "main/input_score/score.html"
    success_url = reverse_lazy("main:input_score_page")

    def get_object(self, queryset=None):
        encoded_pk = self.kwargs.get('encoded_pk')  
        decoded_pk = unquote(encoded_pk)
        return get_object_or_404(self.model, title=decoded_pk) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        score = self.get_object()
        diff = Diff.objects.filter(title=score.title)  
        
        context['diff'] = diff
        
        return context



from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main/login/')  # 登録後にログインページにリダイレクト
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



