import csv
from django.core.management.base import BaseCommand
from importer.models import Product

class Command(BaseCommand):
    help = 'Import name and email from CSV into Person table, skipping rows with errors'

    def handle(self, *args, **kwargs):
        try:
            with open('importer/data.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for index, row in enumerate(reader, start=1):
                    try:
                        name = row['name']
                        price = row['salePrice']
                        description = row['description']
                        image_urls = row['imageUrls']  # Use .get() to avoid KeyError

                        if not name or not price or not description:
                            raise ValueError("Missing data in row")

                        product, created = Product.objects.get_or_create(
                            price=price,
                            description=description,
                            name=name,  # use name in the get_or_create lookup if you want to avoid duplicates better
                            defaults={
                                'image_urls': image_urls
                            }
                        )

                        if created:
                            self.stdout.write(self.style.SUCCESS(f"[Row {index}] Added {name}"))
                        else:
                            # Optional: update image_urls if it's missing or changed
                            if not product.image_urls and image_urls:
                                product.image_urls = image_urls
                                product.save()
                                self.stdout.write(self.style.WARNING(f"[Row {index}] Updated image URLs for {name}"))
                            else:
                                self.stdout.write(self.style.WARNING(f"[Row {index}] {name} already exists"))

                    except Exception as row_error:
                        self.stdout.write(self.style.ERROR(f"[Row {index}] Skipped due to error: {row_error}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("CSV file not found. Please check the path."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))