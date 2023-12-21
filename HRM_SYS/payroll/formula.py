from .models import Payroll_Rates
from decimal import Decimal
import pandas 
import math

tax_formula = '''24000=10,8333=25,467667=30,300000=32.5
'''

def tax_amount(rates,amount,relief):
    if math.isnan(amount) == True:
        amount = 0.00
    first = Decimal(rates.split(',')[0].split("=")[0])
    first_rate = Decimal(rates.split(',')[0].split("=")[1])/100
    second = Decimal(rates.split(',')[1].split("=")[0])
    second_rate = Decimal(rates.split(',')[1].split("=")[1])/100
    third_rate = Decimal(rates.split(',')[2].split("=")[1])/100
    tax=0


    if amount > first and amount <= first+second :

       tax += Decimal((first*first_rate)+(second*second_rate))-relief

    elif amount > (first+second):
        
        tax += Decimal(((amount - first - second )*third_rate)+(first*first_rate)+(second*second_rate))-relief

    elif amount <= first:

        tax += 0

    return tax



def nhif_pay(gross):

    rates = Payroll_Rates.objects.last()
    nhif_amount = 0
    if len(str(rates.nhif_rates_file.url))>0:

        rates_df =  pandas.read_excel(rates.nhif_rates_file.url)

        for i,rows in rates_df.iterrows():

            if pandas.isna(rows["to"])==True:
                if gross >= rows["from"]:

                    nhif_amount = rows["amount"]
            
            else:


                if gross >= rows["from"] and gross <= rows["to"]:

                    nhif_amount = rows["amount"]
    
    return nhif_amount

#print(nhif_pay(20000))

def nssf_pay(gross):

    rates = Payroll_Rates.objects.last()

    nssf_amount = gross*(Decimal(rates.nssf_rate/100))

    return nssf_amount 

def house_levy_pay(gross):

    rates = Payroll_Rates.objects.last()

    levy_amount = gross*(Decimal(rates.house_levy_rate/100))

    return levy_amount

def nhif_relief(nhif,paye):
    rates = Payroll_Rates.objects.last()
    amount = 0
    if paye>0:
        if nhif*(rates.nhif_relief_rate/100) > 5000:
            amount += 5000
        else:
            amount += nhif*(rates.nhif_relief_rate/100)
    else:

        amount+=0

    return amount





