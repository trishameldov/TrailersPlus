from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_auto_20220103_2003'),
    ]

    operations = [
        migrations.RunSQL(
            """BEGIN;
                --
                -- Alter field id on trailertranslation
                --
                ALTER TABLE "product_trailertranslation" ALTER COLUMN "id" TYPE bigint USING "id"::bigint;
                DROP SEQUENCE IF EXISTS "product_trailertranslation_id_seq" CASCADE;
                CREATE SEQUENCE "product_trailertranslation_id_seq";
                ALTER TABLE "product_trailertranslation" ALTER COLUMN "id" SET DEFAULT nextval('"product_trailertranslation_id_seq"');
                SELECT setval('"product_trailertranslation_id_seq"', MAX("id")) FROM "product_trailertranslation";
                ALTER SEQUENCE "product_trailertranslation_id_seq" OWNED BY NONE;
                COMMIT;""",
            state_operations=[
                migrations.AlterField(
                    model_name='trailertranslation',
                    name='id',
                    field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID'),
                ),
            ]
        ),
    ]