"""
Created on Tue Feb 25 22:52:44 2020

@author: Mecit
"""


"""
Resources:
    -- from functools import partial --

    When the create buttons with for loop, ( command= lambda : *args ) is not working.
    There is 2 ways to handle it.
    One of them is .bind method other one is partial method.
    Partial method works like that -> partial(function_name,parameeter)
    As a result program can underestand easily which button pressed.
"""


from tkinter import *
# import msgpack
import pickle
import dbm
from functools import partial
from tkinter import ttk


class RestaurantSystem(Frame):
    all_rest=[]
    def __init__(self,parent):
        """
        
        Arguments:
            Frame {Root} -- tkinter Frame
            parent {frame Root} -- frame Root

            all_rest {list} -- it storage all the restaurant object
            database {dbm} -- database file
    
        Returns:
            None

        """        
        Frame.__init__(self,parent)
        self.parent=parent
        self.pack()
        self.database=dbm.open('RestaurantSystemm.db',"c")
        if len(self.database) != 0:
            get_list=self.database['System']
            get_converted_list=pickle.loads(get_list)
            for get_objects in get_converted_list:
                self.all_rest.append(get_objects)
            # print(pickle.loads(self.database['Av Foods']))
            self.av_foods = pickle.loads(self.database['Av Foods'])
            self.av_drink = pickle.loads(self.database['Av Drinks'])
        else:
            empty_list=[] 
            convert=pickle.dumps(empty_list)
            self.database["System"]=convert
            self.av_foods = {'Makarna':25,'Fajita':55,'Hamburger':30}
            self.av_drink = {'Coca Cola':5,'Water':1}
        
        """ 
        Context : Foods Menus
        """
        self.variation = {'Foods':self.av_foods,'Drinks':self.av_drink}
        
        print(self.variation)

        self.initGUI()
    

    def initGUI(self):
        """
        Labels:
            BIG_TEXT - RESTURANT RESERVATION SYSTEM
            rest_name_label - RESTAURANT NAME LABEL
            num_of_tables_label - NUM OF TABLES LABEL
            rst - RESTAURANT LABEL FOR COMBOBOX
            table_label - WHICH TABLE SELECTED LABEL
            cust_name_label - CUSTOMER NAME LABEL
            cust_phone_label - CUSTOMER PHONE  NUMBER LABEL
            test_delete - WARNING LABEL (INCOMPLETE INFORMATIN , SELECTED TABLE FIRST  ETC .. )
            table_must_int  -  WARNING LABEL (TABLE NUMBER MUST BE INTEGER OR TABLE NUM 6 OR 24 ETC.. )
            are_you_sure_label  - ARE YOU SURE LABEL IF THE DELETE RESTAURANT CLICKED.

        Entries:
            rest_name_entry - RESTAURANT NAME ENTRY
            num_of_tables_entry - NUM OF TABLES ENTRY
            cust_name_entry -  CUSTOMER NAME ENTRY
            cust_phone_entry  - CUSTOMER PHONE NUMBER ENTRY

        Buttons:
            create_rest_button - CREATE RESTAURANT BUTTON 
            save_button -  SAVE (RESERVE) BUTTON
            delete_reserv - DELETE RESERVATION BUTTON
            delete_from_combobox - DELETE RESTAURANT BUTTON

        """        
        
        self.BIG_TEXT=Label(self,text="Restaurant Reservation System",bg="blue",fg="white",font=("Helvetica",14,"bold"),anchor=CENTER)
        self.BIG_TEXT.grid(row=0,column=0,columnspan=8,sticky=E+W+S+N)
        
        self.rest_name_label=Label(self,text="Restaurant Name:")
        self.rest_name_label.grid(row=1,column=0,sticky=E+W+S+N,padx=20,pady=10)

        self.rest_name_entry=Entry(self)
        self.rest_name_entry.grid(row=1,column=1,sticky=E+W+S+N,pady=10)


        self.num_of_tables_label=Label(self,text="Number Of Tables:")
        self.num_of_tables_label.grid(row=1,column=2,sticky=E+W+S+N,pady=10)
        

        self.num_of_tables_entry=Entry(self)
        self.num_of_tables_entry.grid(row=1,column=3,sticky=E+W+S+N,pady=10)

        self.create_rest_button=Button(self,text="Create New Restaurant",command=self.create_new_restaurant)
        self.create_rest_button.grid(row=1,column=4,sticky=E+W+S+N,padx=30,pady=10)

        self.rst=Label(self,text="Restaurant:")
        self.rst.grid(row=2,column=0,sticky=E+W+S+N,pady=10)
        self.select_combobox=ttk.Combobox(self,values=self.all_rest) 
        self.select_combobox.grid(row=2,column=1)
        self.select_combobox.bind("<<ComboboxSelected>>",self.create_tables_frame)
        
        self.delete_from_combobox=Button(self,text="Delete Restaurant" , command=self.delete_combobox ,padx=1,pady=1)
        self.delete_from_combobox.grid(row=2,column=2 ,sticky=E+W+S+N, padx= 20 ,pady = 5)
        
        self.are_you_sure_label=Label(self,text="")
        self.are_you_sure_label.grid(row=2,column=3, sticky=E+W+S+N)

        self.table_label_variable=StringVar()
        self.table_label_variable.set("Table: [NOT SELECTED]")
        self.table_label=Label(self,textvariable=self.table_label_variable)
        self.table_label.grid(row=3,column=0,padx=20,sticky=E+W+S+N)

        self.cust_name_label=Label(self,text="Customer Name:")
        self.cust_name_label.grid(row=3,column=1,sticky=E+W+S+N)

        self.cust_name_entry=Entry(self)
        self.cust_name_entry.grid(row=3,column=2,padx=20,sticky=E+W+S+N)

        self.cust_phone_label=Label(self,text="Customer Phone Number:")
        self.cust_phone_label.grid(row=3,column=3,sticky=E+W+S+N)

        self.cust_phone_entry=Entry(self)
        self.cust_phone_entry.grid(row=3,column=4,sticky=E+W+S+N)

        self.garson_add = Button(self,text="Add Food-Drink to Menu",command=self.add_garson_menu)
        self.garson_add.grid(row=2,column=6,padx=10,pady=10)
        
        self.save_button=Button(self,text="Save/Update Changes",command=self.control_entries)
        self.save_button.grid(row=3,column=5,padx=20,sticky=E+W+S+N)

        self.delete_reserv=Button(self,text="Delete Reservation",command=self.delete_reserve)
        self.delete_reserv.grid(row=3,column=6,padx=20,sticky=E+W+S+N)

        self.add_order = Button(self,text="Add Order",command=self.add_order)
        self.add_order.grid(row=3,column=7,padx=20,sticky=E+W+S+N)

        # self.test_delete=Label(self,text="")
        # self.test_delete.grid(row=3,column=7)

        self.table_must_int=Label(self,text="",anchor=CENTER)
        self.table_must_int.grid(row=1,column=5,sticky=S+W+E+N,columnspan=3,pady=10,padx=10)

        self.tables_numb=0
    

    def add_garson_menu(self):
        if self.select_combobox.get() != "":
            new_toplv  = Toplevel(self)
            
            ot_fR = Frame(new_toplv,relief=GROOVE,borderwidth=3)
            ot_fR.grid(row=0,column=0,padx=10,pady=10)

            variations = ttk.Combobox(ot_fR)
            variations.grid(row=0,column=0,padx=10,pady=10,sticky=S)
            variations.configure(values = ['Foods','Drinks'])
            variations.bind("<<ComboboxSelected>>",self.garson_variatons)
            variations.current(0)
            self.f_p = self.variation[variations.get()]
            
            

            self.av_listbox = Listbox(ot_fR,width=30)
            self.av_listbox.grid(row=1,column=0,padx=10,pady=10,sticky=N)
            self.av_listbox.bind("<<ListboxSelect>>",self.listbox_event)
            self.av_listbox.delete(0,END)

            for foods,price in self.f_p.items():
                string = f'{foods} - {price}$'
                self.av_listbox.insert(END,string)

            
            self.Delete_av_Menu = Button(ot_fR,text="Delete From Available Foods Menus",
                            command = lambda : self.add_or_delete(current_c = variations ,add=False,delete_d=[self.selected_foods],combobox=variations.get()))
            self.Delete_av_Menu.grid(row=2,column=0,padx=10,pady=10,sticky=N)
            
            fR = Frame(new_toplv,relief=GROOVE,borderwidth=3)
            fR.grid(row=0,column=1,padx=10,pady=10)

            Label(fR,text="Add New Foods",bg="green").grid(row=0,column=0,padx=10,pady=10,sticky=E+W+S+N,columnspan=2)
            Label(fR,text="Categories :").grid(row=1,column=0,padx=10,pady=10,sticky=E)
            
            categ = ttk.Combobox(fR,width=17)
            categ.grid(row=1,column=1,padx=10,pady=10,sticky=W)
            categ.configure(values=['Foods','Drinks'])

            Label(fR,text="Food Name : ").grid(row=2,column=0,padx=10,pady=10,sticky=E)
            f_name_ent = Entry(fR)
            f_name_ent.grid(row=2,column=1,padx=10, pady=10,sticky=W)

            Label(fR, text="Money $ : ").grid(row=3,column=0,padx=10,pady=10,sticky=E)
            money_ent = Entry(fR)
            money_ent.grid(row=3,column=1,padx=10,pady=10,sticky=W)

            self.add_new_food_but = Button(fR,text="Add New Foods To Menu",
                command=lambda:self.add_or_delete(current_c = variations , add=True,combobox=categ.get(),add_d={'Cat':categ.get(),'Food Name':f_name_ent.get(),'Money':money_ent.get()}))
            self.add_new_food_but.grid(row=4,column=0,padx=10,pady=10,sticky=E+W+S+N,columnspan=2)
        



        else:
            self.table_must_int.configure(text="First Select Restaurant",bg="red")
            self.originals_settings_buttons(self.table_must_int)
        

    def add_or_delete(self,current_c,combobox,add=False,delete_d=None,add_d=None):
        if add:
            cat = add_d['Cat']
            if cat  == 'Foods':
                f_or_drink = self.av_foods
            elif cat == 'Drinks':
                f_or_drink = self.av_drink
            f_or_drink[add_d['Food Name']] = int(add_d['Money'])
        else:
            cats = self.variation[combobox]
            del cats[self.selected_foods]
        

        self.av_listbox.delete(0,END)
        self.f_p = self.variation[current_c.get()]
        for foods,price in self.f_p.items():
            string = f'{foods} - {price}$'
            self.av_listbox.insert(END,string)
        self.convert_to_dumps()

    def add_order(self):
        
        foods_toplvl = Toplevel(self)
        
        current_restaurant_obj = self.find_combo(self.select_combobox.get())
        self.current_customer_obj = current_restaurant_obj.restaurant_details[self.tables_numb]['Customer']
    
        Label(foods_toplvl,text="Orders",anchor=CENTER,bg="green",fg="black").grid(row=0,column=0,padx=10,pady=10,sticky=E+W+S+N,columnspan=5)
        
        # Label(foods_toplvl,text="Available Foods").grid(row=1,column=0,padx=10,pady=10,sticky=S)
        
        f = Frame(foods_toplvl,relief=GROOVE,borderwidth=3)
        f.grid(row=1,column=0,padx=10,pady=10)
        variation = ttk.Combobox(f)
        variation.grid(row=1,column=0,padx=10,pady=10,sticky=S)
        variation.configure(values = ['Foods','Drinks'])
        variation.bind("<<ComboboxSelected>>",self.get_variations)
        variation.current(0)
        self.f_p = self.variation[variation.get()]
        print(self.f_p)

        
        self.available_foods_listbox = Listbox(f,width=30)
        self.available_foods_listbox.grid(row=2,column=0,padx=10,pady=5,sticky=N,rowspan=2)
        self.available_foods_listbox.bind("<<ListboxSelect>>",self.listbox_event)
        self.available_foods_listbox.delete(0,END)

        for foods,price in self.f_p.items():
            string = f'{foods} - {price}$'
            # string  = f'{foods.food_name} - x{foods.pieces}'
            self.available_foods_listbox.insert(END,string)


        
        self.current_amount = 1
        # self.selected_food_obj.pieces = self.current_amount
        make_order = Button(f,text="Create Order",command=self.make_ord)
        make_order.grid(row=2,column=1,padx=10,pady=10,columnspan=3,sticky=S)

        decresase_amount = Button(f,text="Decresase Amount",command = lambda: self.amount_handler(increase=False))
        decresase_amount.grid(row=3,column=1,padx=10,pady=10,sticky=N)
        self.current_amount_Label = Label(f,text=str(self.current_amount))
        self.current_amount_Label.grid(row=3,column=2,padx=10,pady=10,sticky=N)

        increse_amount = Button(f,text="Increase Amount",command = lambda : self.amount_handler(increase=True))
        increse_amount.grid(row=3,column=3,padx=10,pady=10,sticky=N)

        informations_FR  = Frame(foods_toplvl,relief=GROOVE,borderwidth=3)
        informations_FR.grid(row=1,column=4,padx=10,pady=10,rowspan=2)

        Label(informations_FR,text=f'Customer Name : {self.current_customer_obj.cust_name}').grid(row=0,column=0,padx=10,pady=10)
        Label(informations_FR,text=f'Customer Phone : {self.current_customer_obj.cust_phone}').grid(row=1,column=0,padx=10,pady=10)

        Label(informations_FR,text="Orders").grid(row=2,column=0,padx=10,pady=20,sticky=E+W+S+N)

        self.orders_listbox = Listbox(informations_FR,width=33)
        self.orders_listbox.grid(row=3,column=0,padx=10,pady=10)
        self.orders_listbox.delete(0,END)
        total_bill = 0
        if len(self.current_customer_obj.orders) > 0:
            for ords in self.current_customer_obj.orders:
                string  = f'{ords.food_name} - x{ords.pieces} = {ords.calculate_price()}$'
                self.orders_listbox.insert(END,string)
        
            total_bill = self.current_customer_obj.calculate_total_price()
        self.billLABEL = Label(informations_FR,text=f"Total Price : {total_bill}$")
        self.billLABEL.grid(row=4,column=0,padx=10,pady=10,sticky=E+W+S+N)
    def get_variations(self,event):
        variation= event.widget
        self.f_p = self.variation[variation.get()]
        print(self.f_p)
        self.available_foods_listbox.delete(0,END)
        for foods,price in self.f_p.items():
            string = f'{foods} - {price}$'
            # string  = f'{foods.food_name} - x{foods.pieces}'
            self.available_foods_listbox.insert(END,string)
    def garson_variatons(self,event):
        variation= event.widget
        self.f_p = self.variation[variation.get()]
        self.av_listbox.delete(0,END)
        for foods,price in self.f_p.items():
            string = f'{foods} - {price}$'
            self.av_listbox.insert(END,string)
    def make_ord(self):
        self.selected_food_obj = Foods(food_name=self.selected_foods,food_price=self.f_p[self.selected_foods])
        self.current_customer_obj.make_order(self.selected_food_obj,self.current_amount)
        self.orders_listbox.delete(0,END)
        for ords in self.current_customer_obj.orders:
            string  = f'{ords.food_name} - x{ords.pieces} = {ords.calculate_price()}$'
            self.orders_listbox.insert(END,string)
        self.billLABEL.configure(text=f"Total Price : {self.current_customer_obj.calculate_total_price()}$")
        self.convert_to_dumps()

    def amount_handler(self,increase):
        # pass
        if increase is True:
            self.current_amount_Label.configure(text=str(self.current_amount+1))
            self.current_amount+=1
        elif increase is False:
            self.current_amount_Label.configure(text=str(self.current_amount-1))
            self.current_amount-=1
    def listbox_event(self,event):
        try:
            capture_food=event.widget
            index_food=capture_food.curselection()
            print(index_food)
            food_selected = capture_food.get(index_food)
            self.selected_foods = food_selected.split("-")[0].strip()
            # self.selected_food_obj = Foods.available_foods_dict[food_selected]
            # self.selected_food_obj = 
            # print(self.selected_food_obj)
            self.current_amount = 1
            # self.selected_food_obj.pieces = self.current_amount
            try:
                self.current_amount_Label.configure(text=str(self.current_amount))
            except:pass
        except:pass
    def originals_settings_buttons(self,buttons_name):
        """
        
        Arguments:
            buttons_name {tkinter.Button} -- buttons widget
        Notes:
            This function after the give information to Admin,
            Destroy text in 1.5 seconds with background SystemButtonFace which is Default.
        """        
        self.after(1500,lambda: buttons_name.configure(text="" , bg = "SystemButtonFace"))
    def create_new_restaurant(self):
        """
        Notes:
            If the conditions is True which are Restaurant Name Cannot be empty,
            Also restaurant tables should be integer. If those conditions are True;
            Restaurant will be created as a type of object.
        """        
        if self.rest_name_entry.get() != '':
            try:
                self.convert_int=int(self.num_of_tables_entry.get())
            except:
                self.table_must_int.configure(text="Table Number Must Number!",bg="red",fg="white")
                self.originals_settings_buttons(self.table_must_int)
            else:
                if self.convert_int > 24 or self.convert_int < 6 :
                    self.table_must_int.configure(text="Num. of Tables May Be Between 6 and 24!",bg="red")
                    self.originals_settings_buttons(self.table_must_int)
                else:
                    self.new_rest=self.rest_name_entry.get()
                    self.table_must_int.configure(text="Restaurant Created",bg="green")
                    self.originals_settings_buttons(self.table_must_int)
                    rest_name=self.rest_name_entry.get()
                    self.test_rest_name=rest_name
                    self.test_rest_name=NewRestaurant(rest_name,self.convert_int,{})
                    self.select_combobox.configure(values=self.all_rest)
                    self.convert_to_dumps()
        else:
            self.table_must_int.configure(text="Incomplete Information." , bg = "red")
            self.originals_settings_buttons(self.table_must_int)
    def create_tables_frame(self,event):
        """
        
        Arguments:
            event {class} -- Check The Combobox selected or not?
        
        Notes:
            Create a frame for the restaurant tables.
        """        
        self.new_frame=Frame(self,borderwidth=3,relief=GROOVE)
        self.new_frame.grid(row=4,column=0,columnspan=8,pady=20,sticky=E+W+N+S,padx=20)
        self.create_tables()

    def find_combo(self,find):
        """
        
        Arguments:
            find {str} -- check Combobox.get()
        
        Returns:
            object -- Returns current combobox selected object.
        """        
        for obj_find in self.all_rest:
            if obj_find.rest_name == find:
                self.founded=obj_find
                return self.founded

    def delete_combobox(self):
        """
        Notes:
            This Function When de Admin Click Delete Restaurant Button will Run after that that function create
            One Label
            Two Buttons  which are "Yes" and "No"
            if the Admin click "Yes" :
                get_delete_from_combobox function will run.
            else :
                not_delete_combobox function will run.

        """        
        self.are_you_sure_label.configure(text="Are You Sure?")
        self.yes=Button(self,text="Yes",command=self.get_delete_from_combobox,padx=20)
        self.yes.grid(row=2,column=4)
        self.no=Button(self,text="No",command=self.not_delete_combobox , padx=20)
        self.no.grid(row=2,column=5)

    def get_delete_from_combobox(self):
        """
        Notes:
            If the Admin wants to delete Restaurant , This function provide to delete Restaurant from
            Combobox. Also it's delete from Databases.
        """        
        get_restaurant=self.find_combo(find=self.select_combobox.get())
        if get_restaurant is not None:
            for a in self.all_rest:
                if a == get_restaurant:
                    self.all_rest.remove(get_restaurant)
                    self.table_must_int.configure(text="Restaurant Removed." , bg="yellow")
                    self.originals_settings_buttons(self.table_must_int)
                    self.select_combobox.configure(values=self.all_rest)
                    self.not_delete_combobox()
                    self.new_frame.destroy()
        else:
            self.table_must_int.configure(text="Select Restaurant to Remove!",bg="yellow")
            self.originals_settings_buttons(self.table_must_int)
        self.convert_to_dumps()
    def not_delete_combobox(self):
        """
        Notes:
            If The admin wants to delete  Restaurant but after that admin give up from the deleting decision
            this function useful for preventing to delete Restaurant.
        """        
        self.are_you_sure_label.config(text="")
        self.yes.destroy()
        self.no.destroy()
    def create_tables(self):
        """
        Notes:
            It will  create tables automatically with for loop.
            It automatically find tables number from the NewRestaurant object 'num_of_tables' arguments.
        """        
        rowy=4
        columnx=5
        self.all_buttons=[]
        text_numb=1
        variables_test=1
        restaurant_nam=self.find_combo(find=self.select_combobox.get())
        for a in range(restaurant_nam.num_of_tables):
            string=str(text_numb)
            string=Button(self.new_frame,text=text_numb,padx=20,pady=20,bg="green",command=partial(self.tables_selected,text_numb),anchor=CENTER)
            string.grid(row=rowy,column=columnx,padx=40,pady=15,sticky=E+W+N+S)
            if variables_test%8 == 0:
                rowy+=1
                variables_test=0
                columnx=4
            columnx+=1
            variables_test+=1
            text_numb+=1
            self.all_buttons.append(string)

        self.check_reserved_before()
    def tables_selected(self,tables_number):
        """
        
        Arguments:
            tables_number {int} -- Tables Number From The Button Command
        
        Notes:
            If the Tables Selected This function automatically will run.
            Because of the 'command' parameeter.
            It will return Customer Name and Customer Phone information to the Entries.
        """        
        self.table_label_variable.set(f'Table:{tables_number}')
        self.tables_numb=tables_number
        get_obj=self.find_combo(self.select_combobox.get())
        get_cst=get_obj.restaurant_details.get(self.tables_numb)
        get_info=get_cst.get('Customer')
        if get_info == '':
            self.cust_name_entry.delete(0,END)
            self.cust_phone_entry.delete(0,END)
        else:
            self.cust_name_entry.delete(0,END)
            self.cust_phone_entry.delete(0,END)
            self.cust_name_entry.insert(0,get_info.cust_name)
            self.cust_phone_entry.insert(0,get_info.cust_phone)

    def control_entries(self):
        """
        
        Notes:
            Check Customer Name, Customer Phone Entries are succesfully correct
            in terms of phone number [int].
            Also tables not selected. If other entries completed but tables not selected
            ...error will shown in the Frame.
        """        
        if self.tables_numb == 0:
            self.table_must_int.configure(text="Select Table First",bg="yellow")
            self.originals_settings_buttons(self.table_must_int)
        else:
            if self.cust_name_entry.get() != '':
                try:
                    phone_int=int(self.cust_phone_entry.get())
                except:
                    self.table_must_int.configure(text="MUST ONLY INTEGER",bg="red")
                    self.originals_settings_buttons(self.table_must_int)
                else:
                    self.get_reserve()
            else:
                self.table_must_int.configure(text="INCOMPLETE INFO",bg="red")
                self.originals_settings_buttons(self.table_must_int)

    def get_reserve(self):
        """
        Notes:
            If the all Conditions are True which are 'control_entires' and etc..
            Tables will reserved and it will be saved on current restaurant object dictionary.

        """        
        create_cust_obj_name=self.cust_name_entry.get()
        create_cust_obj_phone=int(self.cust_phone_entry.get())
        customer=Customer(create_cust_obj_name,create_cust_obj_phone)
        current_rest=self.find_combo(find=self.select_combobox.get())
        current_rest.restaurant_details.update({self.tables_numb:{'Customer':customer}})
        self.all_buttons[self.tables_numb-1].configure(bg="red")
        self.table_must_int.configure(text="Reservation created",bg="green")
        self.originals_settings_buttons(self.table_must_int)
        self.convert_to_dumps()

    def check_reserved_before(self):
        """
        Notes:
            When the combobox change, it will identify automatically from the Restaurant Object Dictionary
            Tables are reserved or not?
            If Tables are reserved:
                change tables color and fill with the customer information.
        """        
        rest_name=self.find_combo(self.select_combobox.get())
        for roam in rest_name.restaurant_details:
            get_current_table=rest_name.restaurant_details.get(roam)
            get_cust_name=get_current_table.get('Customer')
            if get_cust_name != '':
                self.all_buttons[roam-1].configure(bg="red")
    def delete_reserve(self):
        """
        Notes:
            It will remove reserved tables from the current Restaurant Object dictionary.

        """        
        current_res=self.find_combo(find=self.select_combobox.get())
        if self.tables_numb != 0:
            current_res.restaurant_details.update({self.tables_numb:{'Customer':''}})
            self.all_buttons[self.tables_numb-1].configure(bg="green")
            self.table_must_int.configure(text="Reservation Deleted",bg="blue")
            self.originals_settings_buttons(self.table_must_int)
            self.convert_to_dumps()
        else:
            self.table_must_int.configure(text="Select Table First.",bg="Yellow")
            self.originals_settings_buttons(self.table_must_int)
    
    def convert_to_dumps(self):
        """
        Notes:
            This function make our system Real-Time Based.
            It will automatically save all motion step by step.
            When the restaurant created it will save.
            When the customer reserve a table it will automatically update system.
        """        
        get_noncv_list=self.database['System']
        get_converted=pickle.loads(get_noncv_list)
        get_converted=[]
        for a in self.all_rest:
            get_converted.append(a)
        get_dumps=pickle.dumps(get_converted)
        self.database['System']=get_dumps

        self.database['Av Foods'] = pickle.dumps(self.av_foods)
        self.database['Av Drinks'] = pickle.dumps(self.av_drink)

class NewRestaurant:
    def __init__(self,rest_name,num_of_tables,restaurant_details):
        """
        
        Arguments:
            rest_name {str} -- Restaurant Name
            num_of_tables {int} -- How much tables belong to this restaurant.
            restaurant_details {dict} -- it Storage Tables , Also Customers.
        """        
        self.rest_name=rest_name
        self.num_of_tables=int(num_of_tables)
        self.restaurant_details=restaurant_details
        self.make_dictionary()
        RestaurantSystem.all_rest.append(self)
    def make_dictionary(self):
        for k in range(self.num_of_tables):
            self.restaurant_details[k+1]={'Customer':''}

    def __repr__(self):
        return self.rest_name

class Foods:
    # available_foods_list = []
    # available_foods_dict = {}
    def __init__(self,food_name,food_price):
        """
        Args:
            food_name (str): food_name
            food_price (int): food_price
        """        
        self.food_name = food_name
        self.food_price = food_price
        self.pieces = 1
        # Foods.available_foods_list.append(self)
        # Foods.available_foods_dict[self.food_name] = self
    def calculate_price(self):
        return self.food_price*self.pieces
    def __repr__(self):
        return self.food_name

class Customer:
    total_bill = 0
    def __init__(self,cust_name,cust_phone):
        """
        
        Arguments:
            cust_name {str} -- Customer Name
            cust_phone {int} -- Customer Phone Number
        """        
        self.cust_name=cust_name
        self.cust_phone=cust_phone
        self.orders = []
        self.orders_dict = {}
    def calculate_total_price(self):
        # if len(self.orders) > 0:
        #     for food_objects in self.orders:
        #         self.total_bill+=food_objects.calculate_price()
        return self.total_bill
    def order_cancellation(self,food_obj):
        # if food_obj.food_name in Foods.available_foods_dict:
            # current_food = Foods.available_foods_dict[food_name]
        self.total_bill-=food_obj.calculate_price()
        self.orders.remove(food_obj)
    def make_order(self,food_obj,amount):
        # if food_obj.food_name in Foods.available_foods_dict:
            # current_food = Foods.available_foods_dict[food_name]
        food_obj.pieces = amount
        self.total_bill+=food_obj.calculate_price()
        self.orders.append(food_obj)
        self.orders_dict[food_obj] = food_obj.pieces
        print("Orders Created")
        print(self.orders)
        
    def __repr__(self):
        return self.cust_name


if __name__ == "__main__":
    root = Tk()
    root.title("Restaurant System")
    System=RestaurantSystem(root)
    root.mainloop()

