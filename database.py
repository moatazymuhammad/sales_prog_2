from peewee import *

db=MySQLDatabase('sales_prog', user='root',
                 password='toor',host='localhost',port=3306)

####################################
#################################### adding tables

class items(Model): ################ add new item
        name=CharField(null=True)
        special_code=CharField(null=True)
        pur_price=FloatField(null=True)
        sell_price=FloatField(null=True)
        fast_code=CharField(null=True)
        barcode=CharField(null=True)
        req_quan=IntegerField(null=True)
        comment=TextField(null=True)
        have_expiry=TextField(null=True)
        class Meta:
            database= db


class clients(Model):################ add new client
        name=CharField(null=True)
        phone=CharField(null=True)
        comment=TextField(null=True)
        class Meta:
            database= db

class vendors(Model):################ add new vendor
        name=CharField(null=True)
        phone=CharField(null=True)
        comment=TextField(null=True)
        class Meta:
            database= db


class depository(Model):################ add new depository
        name=CharField(null=True)
        belong=CharField(null=True)
        comment=TextField(null=True)
        class Meta:
            database= db

class branch(Model):################ add new branch
        name=CharField(null=True)
        comment=TextField(null=True)
        class Meta:
            database= db

class employees(Model):################ add new employee
        name=CharField(null=True)
        password=CharField(null=True)
        branch=CharField(null=True)
        dedicate=CharField(null=True)
        adminity=CharField(null=True)
        join_date=DateField(null=True)
        comment=TextField(null=True)
        auth1=CharField(null=True)
        auth2=CharField(null=True)
        auth3=CharField(null=True)
        auth4=CharField(null=True)
        auth5=CharField(null=True)
        auth6=CharField(null=True)
        auth7=CharField(null=True)
        auth8=CharField(null=True)
        auth9=CharField(null=True)
        auth10=CharField(null=True)
        auth11=CharField(null=True)
        class Meta:
            database= db

####################################
#################################### moves tables

class safe_moves(Model):################ track safe moves
        branch=CharField(null=True)#save branch
        reason=CharField(null=True)
        amount=FloatField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        comment=TextField(null=True)
        employee=CharField(null=True)
        move=CharField(null=True)
        source=CharField(null=True)
        class Meta:
            database= db

class drawer_moves(Model):################ track drawer moves
        branch=CharField(null=True)#save branch
        reason=CharField(null=True)
        amount=FloatField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        comment=TextField(null=True)
        employee=CharField(null=True)
        move=CharField(null=True)
        source=CharField(null=True)
        class Meta:
            database= db

class client_balance(Model):################ track client balance
        name=CharField(null=True)
        amount=FloatField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        move=CharField(null=True)#in or out
        reason=CharField(null=True)
        employee=CharField(null=True)
        branch=CharField(null=True)
        bill_id=CharField(null=True)
        class Meta:
            database= db

class vendor_balance(Model):################ track vendor balance
        name=CharField(null=True)
        amount=FloatField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        move=CharField(null=True)#in or out
        reason=CharField(null=True)
        employee=CharField(null=True)
        branch=CharField(null=True)
        bill_id=CharField(null=True)
        class Meta:
            database= db

class items_moves(Model):################track items moves
        name=CharField(null=True)
        special_code=CharField(null=True)
        amount=IntegerField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        employee=CharField(null=True)# save the working employee
        store1=CharField(null=True)#
        store2=CharField(null=True)#
        move=CharField(null=True)
        operation=CharField(null=True)
        expiry=DateField(null=True)
        reason=CharField(null=True)
        
        
        class Meta:
            database= db

class bill_no(Model):################track items moves
        number=CharField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        employee=CharField(null=True)
        store=CharField(null=True)
        move=CharField(null=True)
        cl_vend=CharField(null=True)
        bill_total=CharField(null=True)
        
        class Meta:
            database= db

class temp_bill(Model):################track items moves
        name=CharField(null=True)
        special_code=CharField(null=True)
        amount=IntegerField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        price=FloatField(null=True)
        employee=CharField(null=True)# save the working employee
        expiry=DateField(null=True)
        store=CharField(null=True)#
        total=FloatField(null=True)
        bill_id=CharField(null=True)
        cl_vend=CharField(null=True)
        move=CharField(null=True)
        cost=FloatField(null=True)
        class Meta:
            database= db

class items_sell(Model):################track items moves
        name=CharField(null=True)
        special_code=CharField(null=True)
        amount=IntegerField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        price=FloatField(null=True)
        employee=CharField(null=True)# save the working employee
        expiry=DateField(null=True)
        store=CharField(null=True)#
        total=FloatField(null=True)
        bill_id=CharField(null=True)
        client=CharField(null=True)
        comment=TextField(null=True)
        class Meta:
            database= db

class items_sell_ret(Model):################track items moves
        name=CharField(null=True)
        special_code=CharField(null=True)
        amount=IntegerField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        price=FloatField(null=True)
        employee=CharField(null=True)# save the working employee
        expiry=DateField(null=True)
        store=CharField(null=True)#
        total=FloatField(null=True)
        bill_id=CharField(null=True)
        client=CharField(null=True)
        comment=TextField(null=True)

        class Meta:
            database= db

class items_pur(Model):################track items moves
        name=CharField(null=True)
        special_code=CharField(null=True)
        amount=IntegerField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        price=FloatField(null=True)
        employee=CharField(null=True)# save the working employee
        expiry=DateField(null=True)
        store=CharField(null=True)#
        total=FloatField(null=True)
        bill_id=CharField(null=True)
        vendor=CharField(null=True)
        comment=TextField(null=True)
        class Meta:
            database= db

class items_pur_ret(Model):################track items moves
        name=CharField(null=True)
        special_code=CharField(null=True)
        amount=IntegerField(null=True)
        date=DateField(null=True)
        time=TimeField(null=True)
        price=FloatField(null=True)
        employee=CharField(null=True)# save the working employee
        expiry=DateField(null=True)
        store=CharField(null=True)#
        total=FloatField(null=True)
        bill_id=CharField(null=True)
        vendor=CharField(null=True)
        comment=TextField(null=True)

        class Meta:
            database= db
            
class item_quant(Model):################ fast quantity
        name=CharField(null=True)
        special_code=CharField(null=True)
        quantity=IntegerField(null=True)
        expiry=DateField(null=True)
        store=CharField(null=True)
        price=FloatField(null=True)
        class Meta:
            database= db

class employee_absence(Model):################ track employee absence
        name=CharField(null=True)#save employee id
        date=DateField(null=True)
        time_in=TimeField(null=True)
        time_out=TimeField(null=True)
        branch=CharField(null=True)
        comment=CharField(null=True)
        
        class Meta:
            database= db

####################################
####################################set defaults table

class default_branch(Model):################ save default values
        branch=CharField(null=True)
        log_date=DateField(null=True)
        log_time=TimeField(null=True)
        class Meta:
            database= db
            
class default_employee(Model):################ save default values
        employee=CharField(null=True)
        log_date=DateField(null=True)
        log_time=TimeField(null=True)
        class Meta:
            database= db

class barcode_table(Model):################ save default values
        barcode=CharField(null=True)
        name=CharField(null=True)
        amount=IntegerField(null=True)
        class Meta:
            database= db

####################################
####################################

db.connect()
db.create_tables([items,clients,vendors,depository,branch,employees,safe_moves,
                  drawer_moves,client_balance,vendor_balance,barcode_table,
                  items_moves,employee_absence,item_quant,
                  default_branch, default_employee,items_sell,
                  items_pur,items_sell_ret,items_pur_ret,temp_bill,bill_no])
