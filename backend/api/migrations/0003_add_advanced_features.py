# Generated migration for advanced features

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_address_parcel_zoning_info_and_more'),
    ]

    operations = [
        # Add new fields to Parcel
        migrations.AddField(
            model_name='parcel',
            name='owner_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='owner_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='listing_type',
            field=models.CharField(choices=[('SALE', 'For Sale'), ('LEASE', 'For Lease'), ('BOTH', 'Sale or Lease')], default='SALE', max_length=10),
        ),
        migrations.AddField(
            model_name='parcel',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Sale price in ETB', max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='lease_price_monthly',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Monthly lease in ETB', max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='lease_price_yearly',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Yearly lease in ETB', max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='price_per_sqm',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Price per square meter', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='is_negotiable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='currency',
            field=models.CharField(default='ETB', max_length=3),
        ),
        migrations.AddField(
            model_name='parcel',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'Available'), ('PENDING', 'Pending'), ('SOLD', 'Sold'), ('LEASED', 'Leased')], default='AVAILABLE', max_length=20),
        ),
        migrations.AddField(
            model_name='parcel',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parcel',
            name='views_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parcel',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        
        # Create ParcelImage model
        migrations.CreateModel(
            name='ParcelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='parcel_images/')),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.parcel')),
            ],
            options={
                'ordering': ['order', '-is_primary', '-uploaded_at'],
            },
        ),
        
        # Create ParcelDocument model
        migrations.CreateModel(
            name='ParcelDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('TITLE_DEED', 'Title Deed'), ('SURVEY', 'Survey Document'), ('PERMIT', 'Building Permit'), ('OTHER', 'Other')], max_length=20)),
                ('file', models.FileField(upload_to='parcel_documents/')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='api.parcel')),
            ],
        ),
        
        # Create NearbyAmenity model
        migrations.CreateModel(
            name='NearbyAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity_type', models.CharField(choices=[('SCHOOL', 'School'), ('HOSPITAL', 'Hospital'), ('MARKET', 'Market'), ('BANK', 'Bank'), ('TRANSPORT', 'Public Transport'), ('RESTAURANT', 'Restaurant'), ('SHOPPING', 'Shopping Center'), ('PARK', 'Park'), ('OTHER', 'Other')], max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('distance_km', models.DecimalField(decimal_places=2, help_text='Distance in kilometers', max_digits=5)),
                ('latitude', models.DecimalField(blank=True, decimal_places=9, max_digits=12, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=9, max_digits=12, null=True)),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='api.parcel')),
            ],
            options={
                'verbose_name_plural': 'Nearby Amenities',
                'ordering': ['distance_km'],
            },
        ),
        
        # Create Inquiry model
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('inquiry_type', models.CharField(choices=[('VIEWING', 'Request Viewing'), ('INFO', 'Request Information'), ('OFFER', 'Make Offer'), ('OTHER', 'Other')], default='INFO', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='api.parcel')),
            ],
            options={
                'verbose_name_plural': 'Inquiries',
                'ordering': ['-created_at'],
            },
        ),
        
        # Create ParcelComparison model
        migrations.CreateModel(
            name='ParcelComparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_session', models.CharField(help_text='Session ID for anonymous users', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parcels', models.ManyToManyField(related_name='comparisons', to='api.parcel')),
            ],
        ),
    ]
