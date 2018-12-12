import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox

class Dictionary:

    def __init__(self,master):
        '''Fungsi utama dari class Dictionary (tampilan GUI)'''
        self.master = master
        self.master.title('WR Definition')
        self.master.minsize(500,300)
        self.__init_label()
        self.__init_entry()
        self.__init_text()
        
    def __init_label(self):
        '''Untuk membuat label.'''
        self.Judul2 = Label(self.master,text='WordReference.com',fg='white',font='Helvetica 24 bold',bg='midnight blue')
        self.Judul2.grid(row=1,column=0,padx=250,columnspan=2)
        self.Judul3 = Label(self.master,text='World’s Leading Online Source for English Definitions',fg='white',font='Times 14',bg='midnight blue')
        self.Judul3.grid(row=2,column=0,columnspan=2)

    def __init_entry(self):
        '''Untuk membuat entri dan memasukan hasil ke dalam variabel.'''
        self.word=StringVar()
        self.Entry=Entry(self.master,textvariable=self.word,width=30)
        self.Entry.grid(row=3,column=0,rowspan=3,pady=10,ipady=10,ipadx=50,columnspan=2)
    

    def __init_text(self):
        '''Membuat widget message.'''
        self.message=Message(self.master,bg='midnight blue',fg='white',text="The English Dictionary",font='Times 14 bold',width=600,justify='center')
        self.message.grid(row=9,column=0,pady=15,columnspan=2)
        self.message1=Message(self.master,bg='midnight blue',fg='white',text="WordReference is proud to offer two English dictionaries--the WordReference Random House Learner's Dictionary of American English and the Collins Concise English Dictionary. These prestigious dictionaries contain more than 125,000 words and phrases.",font='Times 12',width=600,justify='center')
        self.message1.grid(row=10,column=0,pady=5,columnspan=2)
        self.message2=Message(self.master,bg='midnight blue',fg='white',text="Online Languange Dictionaries\nwww.wordreference.com",font='Times 12',width=600,justify='center')
        self.message2.grid(row=11,column=0,pady=5,columnspan=2)
        self.message3=Message(self.master,bg='midnight blue',fg='white',text="Try to search a word or phrase!",font='Times 12 italic',width=600,justify='center')
        self.message3.grid(row=8,column=0,pady=5,columnspan=2)
        
    def text_to_gui(self,petunjuk):
        '''Untuk menampilkan hasil ke GUI dengan widget message.'''
        self.message['text']=petunjuk
        self.n=3
        if self.num>4:
            self.message1['text']=self.arti[:self.arti.find('4.)')]
            self.More=Button(self.master,text='Next',command=self.more,font=('Helvetica','12','bold'),width=10,height=1,fg='midnight blue',bg='white')
            self.More.grid(row=12,column=1,pady=10)
            self.Before=Button(self.master,text='Back',command=self.before,font=('Helvetica','12','bold'),width=10,height=1,fg='midnight blue',bg='white')
            self.Before.grid(row=12,column=0,pady=10)
        else:
            self.message1['text']=self.arti

    def more(self):
        '''Untuk menggeser ke 3 nomor selanjutnya.'''
        self.n+=3
        if  self.n>=self.num:
            self.n=self.num
            if self.num%3==0:
                self.message1['text']=self.arti[self.arti.find(str(self.num-2)+'.)'):]
            else:
                batas=self.num-(self.num%3)
                self.message1['text']=self.arti[self.arti.find(str(batas+1)+'.)'):]
        else:
            self.message1['text']=self.arti[self.arti.find(str(self.n-2)+'.)'):self.arti.find(str(self.n+1)+'.)')]
        
    def before(self):
        '''Untuk menggeser ke 3 nomor sebelumnya.'''
        if self.n>=self.num:
            if self.num%3==0:
                self.n=self.num-3
            else:
                self.n=self.num-(self.num%3)
            self.message1['text']=self.arti[self.arti.find(str(self.n-2)+'.)'):self.arti.find(str(self.n+1))]
        else:
            self.n-=3
            if self.n<=3:
                self.message1['text']=self.arti[:self.arti.find('4.)')]
                self.n=3
            else:
                self.message1['text']=self.arti[self.arti.find(str(self.n-2)+'.)'):self.arti.find(str(self.n+1)+'.)')]
            
    def keyword(self,event):
        '''Menerima keyword'''
        self.key=self.word.get()
        if len(self.key)==0:
            messagebox.showerror("Error","Type word or phrase!")
        else:
            self.web_into_text(self.key)

    def web_into_text(self,key):
        '''Mendapatkan informasi dari web yang dituju dengan kata yang diinginkan'''
        url='http://www.wordreference.com/definition/'
        keyword=key.split(' ')
        if len(key)>1:
            n=0
            for i in range(len(keyword)-1):
                url=url+str(keyword[n])+'%20'
                n+=1
            url=url+str(keyword[n])
        else:
            url=url+str(keyword[0])

        data=requests.get(url).text
        
        soup=BeautifulSoup(data,'html.parser')

        self.num=1

        data_utk_entri=''
        for i in soup.find_all('p'):
            data_utk_entri=data_utk_entri+'\n'+i.get_text().strip()
        
        if 'No dictionary entry found' in data_utk_entri:
            self.message['text']='No dictionary entry found for "'+key+'"!'
            self.message1['text']=''
            self.message3['text']='Try to search a word or phrase!'

        elif "WordReference can't find this exact phrase" in data_utk_entri:
            self.message['text']='We could not find the full phrase you were looking for.'
            self.message1['text']=''
            self.message3['text']='Try to search a word or phrase!'
            
        else:
            text=soup.find_all('span', {'class':'rh_def'})
            
            self.arti=''
            
            self.petunjuk='Definition of "'+key+'" in English :'
            
            for sentence in text:
                meaning=sentence.get_text().strip()
                for tipe in sentence.find_all('span',{'class':'rh_cat'}):
                    tipeku=tipe.get_text()
                    if tipeku in meaning:
                        meaning=meaning.replace(tipeku,'[ '+tipeku+' ] ')

                if ':' in meaning:
                    mean=meaning[:meaning.find(':')].strip()
                    example=meaning[meaning.find(':')+1:].strip()
                    self.arti=self.arti+str(self.num)+".) "+mean+'\nExample :\n'+example+'\n\n'
                    self.num+=1
                else:
                    self.arti=self.arti+str(self.num)+'.) '+meaning+'\n\n'
                    self.num+=1

            self.num-=1

            if self.num>=1:
                if self.num>1:
                    self.message3['text']='We found '+str(self.num)+' results for '+key+'.'
                else:
                    self.message3['text']='We found '+str(self.num)+' result for '+key+'.'
                self.text_to_gui(self.petunjuk)
            else:
                self.message['text']='No dictionary entry found for "'+key+'"!'
                self.message1['text']=''
                self.message3['text']='Try to search a word or phrase!'
                
            
def main():
    root_window=Tk()
    window=Dictionary(root_window)
    window.Entry.bind('<Return>',window.keyword)
    root_window.configure(bg='midnight blue')
    root_window.mainloop()


if __name__=='__main__':
    main()
