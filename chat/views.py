from django.shortcuts import render , redirect , get_object_or_404
from .models import Room , Message
from django.http import HttpResponseRedirect , Http404
from django.urls import reverse
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if pass1 != pass2:
           messages.error(request , 'The two passwords do not match!')
           return redirect('register')
        else:
            user = User.objects.create_user(username=username , email=email , password=pass1)
            user.save()
            login(request,user)
            return redirect('main')
    
    return render(request , 'chat/register.html')   

def loginUser(request):
    
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request,user)  
            return redirect('main')
        else:
            messages.error(request , 'Username or Password doesnt match.')   

    return render(request , 'chat/login.html')

def logoutUser(request):
    
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def main(request):
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('room').lower()

        if username != request.user.username:
            messages.error(request , 'Username does not exist!')
            return redirect('main')

        
        if Room.objects.filter(name=room_name).exists():
            room = Room.objects.get(name=room_name)
            return HttpResponseRedirect(reverse('room', args=[room.id]))
        
        else:

            room = Room.objects.create(
               name = room_name
            )
            
            room.save()
            return HttpResponseRedirect(reverse('room', args=[room.id]))
        
    room_count = Room.objects.all().count()    
                
        
            
    context = {'room_count':room_count}
    return render(request , 'chat/main.html' , context )

@login_required(login_url='login')
def room(request , pk):
    
    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all()
    room_messages_count = room_messages.count()

    if request.method == 'POST':
        room_messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        
        return redirect('room',pk=room.id)

    context = {'room':room , 'room_messages':room_messages , 'room_messages_count':room_messages_count}
    return render(request, 'chat/room.html' , context)



def DeleteMessage(request, pk):
    
    message = Message.objects.get(id=pk)
    

    if request.method == 'POST':
        message.delete()
        return redirect('room',pk=message.room.id)
        
    context = {'message': message}
    return render(request, 'chat/delete.html', context)






    
      


    
