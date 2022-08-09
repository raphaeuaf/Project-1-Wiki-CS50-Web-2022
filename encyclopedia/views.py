from django.shortcuts import render
from sympy import kronecker_product
from django import forms
from django.core.files import File
import random
import markdown2

from . import util


def index(request):
    if request.method == "POST":
        title = request.POST.get("q")
        content = util.get_entry(title)
        dic_ret = {
            "title": title,
            "content": content
        }
        if util.get_entry(title):            
            content = markdown2.markdown(content)
            dic_ret["content"] = content
            return render(request, "encyclopedia/response.html", dic_ret)
        else:
            list = (util.list_entries())
            list_sm = []
            for i in list:
                if title.lower() in i.lower():
                    list_sm.append(i)
            dic_ret["madbra"] = "madbra"
            if list_sm:
                dic_ret["list_sm"] = list_sm
                return render(request, "encyclopedia/apology2.html", dic_ret)
            else:
                return render(request, "encyclopedia/apology.html", dic_ret)
            
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def retrieve(request, title):
    content = util.get_entry(title)
    dic_ret = {
    "title": title,
    "content": content
    }
    if request.method == "GET":
        if util.get_entry(title):            
            dic_ret["content"] = markdown2.markdown(content)
            return render(request, "encyclopedia/response.html", dic_ret)
        else:
            dic_ret["madbra"] = "madbra"
            return render(request, "encyclopedia/apology.html", dic_ret)
    else:
        return render(request, "encyclopedia/editpage.html", dic_ret)


def newpage(request):
    mes = ""
    sa = ""
    ge = ""
    content = ""
    dic_np = {
        "mes": mes,
        "sa": sa,
        "ge": ge,
        "content": content
    }

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("text")
        if not title:
            dic_np["mes"] = "Type a title, "
            dic_np["sa"] = ""
            dic_np["ge"] = "please"
            dic_np["content"] = content
            dic_np["color"] = "red"
            return render(request, "encyclopedia/newpage.html", dic_np)
        elif not request.POST.get("text"):
            dic_np["mes"] = "Your content is blank. "
            dic_np["sa"] = ""
            dic_np["ge"] = "Not like that, bro!"
            dic_np["content"] = content
            dic_np["color"] = "red"
            return render(request, "encyclopedia/newpage.html", dic_np)

        else:
            for i in util.list_entries():
                if title.lower() in i.lower():
                    dic_np["mes"] = "The title '"
                    dic_np["sa"] = title
                    dic_np["ge"] = "' already exists"
                    dic_np["content"] = content
                    dic_np["color"] = "red"
                    return render(request, "encyclopedia/newpage.html", dic_np)
            
            with open(f'entries/{title}.md', 'w', encoding='utf-8') as f:
                myfile = File(f)
                myfile.write(f'# {title}\n\n{content}')

            myfile.closed
            f.closed
            dic_np["mes"] = "The file '"
            dic_np["sa"] = title
            dic_np["ge"] = "' was created successfully"
            dic_np["title"] = title
            content = util.get_entry(title)  
            content = markdown2.markdown(content)
            dic_np["content"] = content
            dic_np["color"] = "green"
            return render(request, "encyclopedia/response.html", dic_np)
    
    else:
        return render(request, "encyclopedia/newpage.html", dic_np)


def editpage(request, methods=["POST"]):
    title = request.POST.get("title")
    content = request.POST.get("text")
    dic_np = {
        "title": title,
        "content": content
    }
    with open(f'entries/{title}.md', 'w', encoding='utf-8') as f:
        myfile = File(f)
        myfile.write(content)

    myfile.closed
    f.closed
    dic_np["mes"] = "The file '"
    dic_np["ge"] = "' was saved successfully"
    dic_np["color"] = "green"    
    dic_np["sa"] = title
    content = util.get_entry(title)  
    content = markdown2.markdown(content)
    dic_np["content"] = content
    return render(request, "encyclopedia/response.html", dic_np)


def randompage(request, methods=["POST"]):
    list_entries = util.list_entries()
    x = random.randint(0, (len(list_entries) - 1))
    title = list_entries[x]
    content = util.get_entry(title)
    content = markdown2.markdown(content)
    dic_ret = {
    "title": title,
    "content": content
    }
    return render(request, "encyclopedia/response.html", dic_ret)