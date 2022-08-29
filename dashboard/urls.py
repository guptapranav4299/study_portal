from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('notes',views.notes,name="notes"),
    path('delete_note/<int:pk>', views.delete_notes, name="delete-note"),
    path('notes_detail/<int:pk>', views.NotesDetailsView.as_view(), name="notes-detail"),
    path('homework', views.homework, name="homework"),


]