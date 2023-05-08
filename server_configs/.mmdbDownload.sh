key=`cat ~/.License_key`

curl -X  GET -o ~/Downloads/city.tar.gz "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=$key&suffix=tar.gz"

cd ~/Downloads/

tar -xf ~/Downloads/city.tar.gz --wildcards '*.mmdb'

rm ~/trailersplus-backend/trailersplus/trailersplus/locations/GeoLite2-City.mmdb

mv ~/Downloads/GeoLite2-City_*/GeoLite2-City.mmdb ~/trailersplus-backend/trailersplus/trailersplus/locations/

rm -r ~/Downloads/GeoLite2-City_*

rm ~/Downloads/city.tar.gz


curl -X  GET -o ~/Downloads/country.tar.gz "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key=$key&suffix=tar.gz"

cd ~/Downloads/

tar -xf ~/Downloads/country.tar.gz --wildcards '*.mmdb'

rm ~/trailersplus-backend/trailersplus/trailersplus/locations/GeoLite2-Country.mmdb

mv ~/Downloads/GeoLite2-Country_*/GeoLite2-Country.mmdb ~/trailersplus-backend/trailersplus/trailersplus/locations/

rm -r ~/Downloads/GeoLite2-Country_*

rm ~/Downloads/country.tar.gz


sudo supervisorctl restart gunicorn
