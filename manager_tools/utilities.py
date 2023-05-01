import re


def import_menu(request):
    menu = []
    labels=set()
    if request.method == "POST":
        file_up = request.FILES["menufile"]
        ext = file_up.name[-3:]
        if ext == 'txt':
            menu = make_from_txt(file_up)
            request.session['menu'] = make_from_txt(file_up)
        elif ext == 'tsv':
            request.session['menu'] = make_from_csv(file_up)
            menu = make_from_csv(file_up)
        else:
            messages.warning(request,"Invalid File Format")
            return render(request,"manager_tools/import.html")
        for line in menu:
            labels.add(line['label'])
            print(labels)
        for label in labels:
            l = Label(name=label)
            l.save()
        for line in menu:
            i = Item(name=line['name'], description=line['description'], price=line['price'], section=line['section'], label=Label.objects.filter(name=line['label']).first())
            i.save()
        return redirect("eat")
    
    return render(request,"manager_tools/import.html")

def make_from_tsv(myfile):
    menu = []
    labels={}

    for line in myfile:
        l =  line.decode('utf-8').rstrip('\n')
        fields = l.split('\t')
        print(fields)
        item = {'section': fields[0], 'label': fields[1], 'name':fields[2], 'description': fields[3], 'price':fields[4].rstrip('\r')}      
        menu.append(item)
    del menu[0]
    return menu

def make_from_txt(myfile):
    menu =[] 
    x = 0
    section = ""
    label = ""
    for line in myfile:
        l =  line.decode('utf-8').rstrip('\n')
        # print(l)
        if l[0] == '-':
            section = l[1:].rstrip('\r')
        elif l[0] == "#":
            label = l[1:].rstrip('\r')
        else:
            if x == 0:
                n = l.rstrip('\r')
            if x == 1:
                d = l.rstrip('\r')
            if x == 2:
                p = l.rstrip('\r')
            x += 1
            if x > 2:
                item = {'section': section, 'label': label, 'name':n, 'description': d, 'price':p}
                menu.append(item)
                x = 0
    del menu[0]
    return menu             
