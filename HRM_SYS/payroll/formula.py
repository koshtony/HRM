from decimal import Decimal
tax_formula = '''24000=10,8333=25,467667=30,300000=32.5
'''

def tax_amount(rates,amount,relief):

    first = float(rates.split(',')[0].split("=")[0])
    first_rate = float(rates.split(',')[0].split("=")[1])/100
    second = float(rates.split(',')[1].split("=")[0])
    second_rate = float(rates.split(',')[1].split("=")[1])/100
    third_rate = float(rates.split(',')[2].split("=")[1])/100
    tax=0
    if amount > first and amount <= first+second :

       tax += Decimal((first*first_rate)+(second*second_rate))-relief

    elif amount > (first+second):
        
        tax += Decimal(((amount - first - second )*third_rate)+(first*first_rate)+(second*second_rate))-relief

    elif amount <= first and amount > 0:

        tax += 0

    return tax






