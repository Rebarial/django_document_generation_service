from django.db import models

class BaseModel(models.Model):
    

    def __str__(self):
        if hasattr(self, 'name') and self.name:
            return self.name
        return f"{self.__class__.__name__} #{self.id}"
    
    def __repr__(self):
        fields = []
        for field in self._meta.fields:
            field_name = field.name
            field_value = getattr(self, field_name)
            fields.append(f"{field_name}: {field_value}")
        return ", ".join(fields)
    
    class Meta:
        abstract = True
        
        
