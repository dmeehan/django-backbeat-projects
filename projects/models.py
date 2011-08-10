# projects/models.py

from django.db import models
from django.db.models import permalink
from django.utils.html import strip_tags

from projects.managers import ProjectManager
from projects.settings import PROJECT_MARKUP

class ProjectBase(models.Model):
    """
    
        An abstract base class for a project.
    
    """
    objects = ProjectManager()
    
    # project status choices 
    STATUS_LIVE = 1
    STATUS_HIDDEN = 2
    STATUS_PENDING = 3
    STATUS_DRAFT = 4
    STATUS_CHOICES = (
        (STATUS_LIVE, 'Live'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_DRAFT, 'Draft'),
        (STATUS_HIDDEN, 'Hidden'),
    )
    
    # Core fields
    name = models.CharField(max_length=250)
    short_description = models.TextField()
    description = models.TextField()
    date_start = models.DateField("start date",
                                  blank=True, null=True,
                                  help_text="Leave blank if project is in promo.")
    date_end = models.DateField("end date",
                                blank=True, null=True,
                                help_text="Leave blank if project is in progress.")

    external_url = models.URLField(blank=True,help_text="Optional.")
    
    # Metadata.
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_LIVE,
                                              help_text="Only projects with live status will be publicly displayed.")
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True,
                            help_text="Suggested value automatically generated from title. Must be unique.")

    #autogenerated fields
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    # Fields to store generated HTML.
    description_html = models.TextField(editable=False, blank=True)
    
    class Meta:
        abstract = True
        ordering = ('-date_end','name',)

    @permalink
    def get_absolute_url(self):
        return ('contacts_contact_detail', [str(self.slug)])
        
    def __unicode__(self):
        return u'%s' % self.name
    
    def render_markup(self):
        """Turns any markup into HTML"""
        original = self.description_html

        if PROJECT_MARKUP == 'markdown':
            import markdown
            self.description_html = markdown.markdown(self.description)
        elif PROJECT_MARKUP == 'textile':
            import textile
            self.description_html = textile.textile(self.description)
        elif PROJECT_MARKUP == 'wysiwyg':
            self.description_html = self.description
        elif PROJECT_MARKUP == 'html':
            self.description_html = self.description
        else:
            self.description_html = strip_tags(self.description)

        return self.description_html != original

    def save(self, force_insert=False, force_update=False):
        self.render_markup()
        super(ProjectBase, self).save(force_insert, force_update)
        
    
class PhysicalProjectBase(ProjectBase):
    """

        A physcially constructable design project. Abstract base model.

    """
    # project size unit choices
    UNIT_SQUAREFOOT = 1
    UNIT_SQUAREMETER = 2
    UNIT_ACRE = 3
    UNIT_HECTARE = 4
    UNIT_CHOICES = (
        (UNIT_SQUAREFOOT, 'square feet'),
        (UNIT_SQUAREMETER, 'square meters'),
        (UNIT_ACRE, 'acres'),
        (UNIT_HECTARE, 'hectares'),
    )
    
    UNIT_CONVERSIONS = {
        (UNIT_SQUAREFOOT, UNIT_SQUAREMETER): .0929,
        (UNIT_SQUAREFOOT, UNIT_ACRE): .000023,
        (UNIT_SQUAREFOOT, UNIT_HECTARE): .0000093,
        (UNIT_SQUAREMETER, UNIT_SQUAREFOOT): 10.76,
        (UNIT_SQUAREMETER, UNIT_ACRE): .00025,
        (UNIT_SQUAREMETER, UNIT_HECTARE): .0001,
        (UNIT_ACRE, UNIT_SQUAREFOOT): 43560,
        (UNIT_ACRE, UNIT_SQUAREMETER): 4047,
        (UNIT_ACRE, UNIT_HECTARE): .4047,
        (UNIT_HECTARE, UNIT_SQUAREFOOT): 107639.10,
        (UNIT_HECTARE, UNIT_SQUAREMETER): 10000.00,
        (UNIT_HECTARE, UNIT_ACRE): 2.47,
    }


    size = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.PositiveSmallIntegerField(choices=UNIT_CHOICES,
                                     default=UNIT_SQUAREFOOT,
                                     help_text="Unit of measurement.")

    size_normalized = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    class Meta:
        abstract = True

    def convert(self, someUnit):
        if someUnit == self.unit:
            return self.unit
        elif (someUnit,self.unit) in self.UNIT_CONVERSIONS:
            return self.unit * self.UNIT_CONVERSIONS[(someUnit,self.unit)]
        else:
            raise Exception("Can't convert")

    @property
    def square_feet(self):
        return self.convert(self.UNIT_SQUAREFOOT)

    @property
    def square_meters(self):
        return self.convert(self.UNIT_SQUAREMETER)

    @property
    def acres(self):
        return self.convert(self.UNIT_ACRE)

    @property
    def hectares(self):
        return self.convert(self.UNIT_HECTARE)

    def save(self, force_insert=False, force_update=False):
        self.size_nomalized = self.convert(self.UNIT_SQUAREFOOT)
        super(PhysicalProjectBase, self).save(force_insert, force_update)
    

