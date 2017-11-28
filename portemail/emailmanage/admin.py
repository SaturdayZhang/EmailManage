from django.forms import ModelForm, TextInput
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from suit.admin import SortableModelAdmin, SortableTabularInline
from suit.widgets import NumberInput, AutosizedTextarea, HTML5Input, EnclosedInput, SuitDateWidget, \
SuitTimeWidget, SuitSplitDateTimeWidget, LinkedSelect
from .models import Ship,Sender,CustomUser,Tonnage,Cargo,Tct,Port,Agent
from .forms import ShipForm


class ShipAdmin(SortableModelAdmin):
    sortable = 'order'
    form = ShipForm
    list_display = ('vessel_name', 'dwt', 'built','type','flag','loa','beam','depth','draft','grain','hatch','tpc')
    search_fields = ('dwt', 'beam')  #在此处设置按照哪些关键字搜索
    list_filter = ('vessel_name', 'flag')
    def suit_row_attributes(self, obj, request):
        return {'class': 'type-%s' % obj.type}
        #通过此方法可以定义div的class等属性值,suit_row_attributes以行为单位，suit_cell_attribute以列为单位
class ShipInline(SortableTabularInline): #使得Ship信息能够根据表头排序
    model = Ship
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-cities'


admin.site.register(Ship,ShipAdmin)
admin.site.register(Tct)
admin.site.register(Port)
admin.site.register(Agent)
admin.site.register(Cargo)
