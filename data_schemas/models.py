from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

COLUMN_SEPARATORS = (
	(",", "Comma(,)"),
	(";", "Semicolon(;)"),
	("|", "Pipe(|)"),
	(" ", "Space( )"),
	("\\t", "Tab(   )"),
)

STRING_CHARACTERS = (
	('"', 'Double Quote(")'),
	("'", "Single Quote(')"),
)

COLUMN_TYPES = (
	("Full Name", "Full Name"),
	("Job", "Job"),
	("Email", "Email"),
	("Domain Name", "Domain Name"),
	("Phone Number", "Phone Number"),
	("Company Name", "Company Name"),
	("Text", "Text"),
	("Integer", "Integer"),
	("Address", "Address"),
	("Date", "Date"),
)


class Schema(models.Model):
	name = models.CharField(max_length=203)
	column_separator = models.CharField(max_length=10, choices=COLUMN_SEPARATORS)
	string_character = models.CharField(max_length=1, choices=STRING_CHARACTERS)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.name}'


class Column(models.Model):
	schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
	name = models.CharField(max_length=202)
	column_type = models.CharField(max_length=20, choices=COLUMN_TYPES)
	from_int = models.IntegerField(blank=True, null=True)
	to_int = models.IntegerField(blank=True, null=True)
	column_order = models.PositiveIntegerField()

	def __str__(self):
		return f'{self.name} - {self.schema.name}'

	def clean(self):
		super().clean()
		if self.column_type == 'Integer' and (self.from_int is None or self.to_int is None):
			raise ValidationError('For integer columns, please provide values for both "from" and "to"')


class CSVFile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	file = models.FileField(upload_to='csv_files/')
	created_date = models.DateField(auto_now_add=True)
	schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.created_date} - {self.schema.name}'
