=====================================
How LILACS was imported into MongoDB
=====================================

---------------------
Fetching the records
---------------------

All records of LILACS were downloaded from the bases.bireme.br server on 
July 25th, 2011, using $ (the CDS/ISIS wildcard symbol) in the advanced
iAH search interface at::

  http://bases.bireme.br/cgi-bin/wxislind.exe/iah/online/?IsisScript=iah/iah.xis&base=LILACS&lang=p&form=A

The search returned 561,811 records, which were downloaded in batches of 
100,000 records or less using ISO-2709 format, resulting in six files::

  -rw-r--r--@ 1 luciano  staff  347515476 Jul 25 22:37 lil2011-100k-00.iso
  -rw-r--r--@ 1 luciano  staff  272541385 Jul 25 22:46 lil2011-100k-01.iso
  -rw-r--r--@ 1 luciano  staff  193464549 Jul 25 22:52 lil2011-100k-02.iso
  -rw-r--r--@ 1 luciano  staff  181640071 Jul 25 22:59 lil2011-100k-03.iso
  -rw-r--r--@ 1 luciano  staff  161673129 Jul 25 23:05 lil2011-100k-04.iso
  -rw-r--r--@ 1 luciano  staff   82610523 Jul 25 23:15 lil2011-100k-05.iso

---------------------------------
Conversion from ISO-2709 do JSON
---------------------------------

The isis2json_ utility was used to convert each file to ISIS-JSON_ type 3 
format::

  $ time isis2json.py -m -t 3 -i 2 -p v lil2011-100k-04.iso > lil2011-04.json

  real    3m12.032s
  user    3m2.342s
  sys     0m1.131s


.. _isis2json: http://github.com/bireme/isis2json
.. _ISIS-JSON: http://reddes.bvsalud.org/projects/isisnbp/wiki/ISIS-JSON_types 


---------------------
Loading into MongoDB
---------------------

Each JSON file was loaded into MongoDB with the ``mongoimport`` utility::

    $ time mongoimport -d lilacs -c type3 lil2011-01.json 
    connected to: 127.0.0.1
                    25577293/323012568      7%
                            6500    2166/second
                    56247167/323012568      17%
                            14500   2416/second
                    87092019/323012568      26%
                            23000   2555/second
                    116912582/323012568     36%
                            31500   2625/second
                    147230676/323012568     45%
                            39800   2653/second
                    176976295/323012568     54%
                            48500   2694/second
                    207098104/323012568     64%
                            57200   2723/second
                    233131861/323012568     72%
                            66400   2766/second
                    260414534/323012568     80%
                            75800   2807/second
                    286497799/323012568     88%
                            86100   2870/second
                    310682381/323012568     96%
                            95400   2890/second
    imported 100000 objects

    real    0m34.138s
    user    0m31.260s
    sys     0m1.334s
    $

After all JSON files are loaded, the MongoDB files for the ``lilacs`` database
look like this::

    $ ls -lah /data/db/lilacs*
    -rw-------  1 luciano  admin    64M Sep  6 23:27 /data/db/lilacs.0
    -rw-------  1 luciano  admin   128M Sep  6 23:27 /data/db/lilacs.1
    -rw-------  1 luciano  admin   256M Sep  6 23:16 /data/db/lilacs.2
    -rw-------  1 luciano  admin   512M Sep  6 23:27 /data/db/lilacs.3
    -rw-------  1 luciano  admin   1.0G Sep  6 23:27 /data/db/lilacs.4
    -rw-------  1 luciano  admin   2.0G Sep  6 23:25 /data/db/lilacs.5
    -rw-------  1 luciano  admin    16M Sep  6 23:27 /data/db/lilacs.ns
    $


-------------------------------
Inspecting the data in MongoDB
-------------------------------

After loading all the records, initial checks are made using the ``mongo`` 
shell::

    $ mongo
    MongoDB shell version: 1.8.3
    connecting to: test
    > use lilacs
    switched to db lilacs
    > db.type3.count();
    561811
    > db.type3.find(null,{'_id':1}).limit(10);
    { "_id" : "593411" }
    { "_id" : "593410" }
    { "_id" : "593409" }
    { "_id" : "593408" }
    { "_id" : "593407" }
    { "_id" : "593406" }
    { "_id" : "593402" }
    { "_id" : "593328" }
    { "_id" : "593405" }
    { "_id" : "593404" }
    > db.type3.findOne();
    {
            "v30" : [
                    {
                            "_" : "Serv. soc. soc"
                    }
            ],
            "v32" : [
                    {
                            "_" : "106"
                    }
            ],
            "v35" : [
                    {
                            "_" : "0101-6628"
                    }
            ],
    [...]
            "_id" : "593411",
            "v5" : [
                    {
                            "_" : "S"
                    }
            ]
    }
    > db.type3.findOne().v35                  
    [ { "_" : "0101-6628" } ]
    > db.type3.findOne()._id
    593411
    > db.type3.findOne().v10
    [
            {
                    "c" : "Florianópolis",
                    "1" : "UFSC",
                    "p" : "Brasil",
                    "3" : "cursos de Graduação Pós-graduação",
                    "2" : "Departamento de Serviço Social",
                    "_" : "Paiva, Beatriz Augusto de"
            }
    ]
    > db.type3.findOne().v12[0]._
    O deciframento de uma realidade em movimento: os caminhos de uma pujante investigação
    >
