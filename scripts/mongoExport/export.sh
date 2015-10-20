OIFS=$IFS;
IFS=",";

dbname=Apps #put "database name" here if you don't want to pass it as an argument

collections=`mongo $dbname --eval "rs.slaveOk();db.getCollectionNames();" --quiet`;
collectionArray=($collections);

for ((i=0; i<${#collectionArray[@]}; ++i));
do
	if [ ${collectionArray[$i]} == "matches" ]; then

    keys=`mongo $dbname --eval "rs.slaveOk();var keys = []; for(var key in db.${collectionArray[$i]}.findOne()) { keys.push(key); }; keys;" --quiet`;
    mongoexport --db $dbname --collection ${collectionArray[$i]} --fields "$keys" --csv --out $dbname.${collectionArray[$i]}.csv;
	else
		echo "not correct DB"

    fi	
done
IFS=$OIFS;