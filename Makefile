.PHONY: syncdbschema createrds deleterds recreaterds deploy

syncdbschema:
	dropdb tweets2text
	createdb tweets2text
	rm -f -r tweets2text/migrations
	python manage.py makemigrations tweets2text
	python manage.py migrate


createrds:
	aws --profile rji-futures-lab rds create-db-instance \
	--db-instance-identifier "tweets-to-text" --db-name "tweets2text" \
	--db-instance-class "db.t2.micro" --engine "postgres" \
	--master-username "postgres" --master-user-password ${DB_PASSWORD} \
	--allocated-storage 20 --vpc-security-group-ids "sg-0f98cf25206b5c515" \
	--tags Key='name',Value='tweets-to-text'
	
	aws --profile rji-futures-lab rds wait db-instance-available \
	--db-instance-identifier "tweets-to-text"

	python manage.py migrate --noinput --settings "config.settings.prod"


deleterds:
	aws --profile rji-futures-lab rds delete-db-instance \
	--db-instance-identifier "tweets-to-text" --skip-final-snapshot \
	--delete-automated-backups
	
	aws --profile rji-futures-lab rds wait db-instance-deleted \
	--db-instance-identifier "tweets-to-text"


recreaterds:
	make deleterds
	
	make createrds


deploy:
	zappa deploy prod

	zappa certify prod

	python manage.py collectstatic --noinput \
	--settings "config.settings.prod"
