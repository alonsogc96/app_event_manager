from rest_framework import permissions

class IsOwnProfileOrAdmin(permissions.BasePermission):
    """
    Permite que un usuario solo pueda editar su propio perfil, a menos que sea administrador.
    También restringe la creación de nuevos usuarios solo a los administradores.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_staff 
        
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        return obj == request.user
