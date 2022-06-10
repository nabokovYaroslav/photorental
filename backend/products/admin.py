from django.contrib import admin
from django.forms import ModelForm, fields, ModelChoiceField, widgets

from products.models import Product, Attribute, EnumGroup, EnumValue, Value, AttributeGroup


class AttributeCommonAdminForm(ModelForm):

    class Meta:
        model = Attribute
        fields = ("datatype",)

class AttributeAdminForm(ModelForm):
    enum_group = ModelChoiceField(label="Группа выбора", queryset=EnumGroup.objects.all(), required=True)
    class Meta:
        model = Attribute
        fields = "__all__"

class AttributeAdminWithoutEnumForm(ModelForm):

    class Meta:
        model = Attribute
        exclude = ("enum_group",)

class AttributeAdmin(admin.ModelAdmin):
        
    def get_form(self, request, obj, **kwargs):
        datatype = request.GET.get("datatype", None)
        if obj:
            if datatype is None:
                if obj.datatype == "enum":
                    return AttributeAdminForm
                return AttributeAdminWithoutEnumForm
            elif datatype == "":
                return AttributeCommonAdminForm
            elif datatype == "enum":
                return AttributeAdminForm
            return AttributeAdminWithoutEnumForm
        else:
            if datatype is None or datatype == "":
                return AttributeCommonAdminForm
            elif datatype == "enum":
                return AttributeAdminForm
            return AttributeAdminWithoutEnumForm

def value_form_factory(request, obj):
    class ValueAdminTextForm(ModelForm):
        value_text = fields.CharField(label="Значение", widget=widgets.Textarea)
        class Meta:
            model = Value
            fields = ("attribute", "product", "value_text")

    class ValueAdminVarcharForm(ModelForm):
        value_varchar = fields.CharField(label="Значение")
        class Meta:
            model = Value
            fields = ("attribute", "product", "value_varchar")

    class ValueAdminEnumForm(ModelForm):

        def get_queryset_for_enum():
            queryset = EnumValue.objects.all()
            attribute = request.GET.get("attribute", None)
            if attribute is not None and attribute != "":
                enum_group_id = Attribute.objects.get(id=attribute).enum_group_id
                return queryset.filter(enum_group_id=enum_group_id)
            if obj:
                enum_group_id = obj.attribute.enum_group_id
                return queryset.filter(enum_group_id=enum_group_id)

        value_enum = ModelChoiceField(label="Значение", queryset=get_queryset_for_enum(), required=True)
        class Meta:
            model = Value
            fields = ("attribute", "product", "value_enum")
            
    attribute = request.GET.get("attribute", None)
    if obj:
        if attribute is not None and attribute == "":
            return ValueAdminCommonForm
        elif attribute is not None and attribute != "":
            datatype = Attribute.objects.get(id=attribute).datatype
            if datatype == "text":
                return ValueAdminTextForm
            if datatype == "varchar":
                return ValueAdminVarcharForm
            if datatype == "enum":
                return ValueAdminEnumForm
        if obj.attribute.datatype == "text":
            return ValueAdminTextForm
        elif obj.attribute.datatype == "varchar":
            return ValueAdminVarcharForm
        elif obj.attribute.datatype == "enum":
            return ValueAdminEnumForm
    else:
        if attribute is not None and attribute == "":
            return ValueAdminCommonForm
        elif attribute is not None and attribute != "":
            datatype = Attribute.objects.get(id=attribute).datatype
            if datatype == "text":
                return ValueAdminTextForm
            if datatype == "varchar":
                return ValueAdminVarcharForm
            if datatype == "enum":
                return ValueAdminEnumForm
        return ValueAdminCommonForm
    

class ValueAdminCommonForm(ModelForm):

    class Meta:
        model = Value
        fields = ("attribute",)

class ValueAdmin(admin.ModelAdmin):
    
    def get_form(self, request, obj, **kwargs):
        return value_form_factory(request, obj)

admin.site.register(Product)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(EnumGroup)
admin.site.register(EnumValue)
admin.site.register(Value, ValueAdmin)
admin.site.register(AttributeGroup)