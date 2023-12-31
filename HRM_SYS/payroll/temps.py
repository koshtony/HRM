from .models import ExtraPayments 
import pandas 

def gen_temp(filename):

    extra_df = pandas.DataFrame(list(ExtraPayments.objects.all().values()))
   

    extra_df["created"] = extra_df["created"].dt.date

    extra_df = extra_df.drop("id",axis=1)

    #extra_df = extra_df.reset_index(drop=True,inplace=False)

    extra_df.to_excel(filename,index=False)