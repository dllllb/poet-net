wget https://linghub.ru/static/Taiga/Taiga_1billion.tar.gz
tar -xzf Taiga_1billion.tar.gz
mv Taiga_1billion/stihi_ru.tar.gz stihi_ru.tar.gz
rm Taiga_1billion.tar.gz
rm -r Taiga_1billion/
tar -xzf stihi_ru.tar.gz
rm stihi_ru.tar.gz
rm -r stihi_ru/tagged