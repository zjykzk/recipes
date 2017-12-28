#!/bin/bash
##########check the paramaters
if [ $# -ne 6 ]; then
	echo $#
	echo "usage: $0 src usr remote_addr remote_dir id_file backupdir"
	exit 1
fi

src=$1
usr=$2
remote_addr=$3
remote_dir=$4
id_file=$5
basename=`basename $src`
dirname=`dirname $src`

# make sure directory exist
ssh -i $id_file $usr@$remote_addr bash -c "'mkdir -p $remote_dir'"

#echo "src:"$src,remote_addr:$remote_addr,remote_dir:$remote_dir",basename:"$basename

echo "#############to transform file $src................."

######### copy to the remote
# create the directory if has
if [ -n $dirname ]; then
  ssh -i $id_file $usr@$remote_addr bash -c "'
  cd $remote_dir
  mkdir -p $dirname
  '"
fi

backupDir=$6
######### backup the file
echo "backup the file $src----------------------"
ssh -i $id_file $usr@$remote_addr bash -c "'
  cd $remote_dir
  if [ ! -e $src ]; then
    exit 1
  fi

  mkdir -p backup
  cd backup
  if [ ! -e $backupDir ]; then
    mkdir $backupDir
  fi

  cd $backupDir
  if [ ! -e $dirname ]; then
    mkdir -p $dirname
  fi

  cd ../../
  cp $src backup/$backupDir/$dirname/
'"


#echo "scp -i "$id_file $src $usr"@"$remote_addr:$remote_dir"/$dirname > /dev/null"
scp -i $id_file $src $usr"@"$remote_addr:$remote_dir"/"$dirname > /dev/null

######## check the result
md5code=`md5sum -b $src | awk '{print $1}'`
#echo "md5sum of "$src
echo $md5code
#echo "------------------"

ret=`ssh $usr@$remote_addr bash -c "'
	cd $remote_dir
  if [ -n $dirname ];then
    cd $dirname
  fi
	md5sum -b $basename
'"`
dest_md5code=`echo $ret | awk '{print $1}'`
#echo "md5sum of dest file"
echo $dest_md5code
#echo "------------------"

if [[ "$md5code" != "$dest_md5code" ]]
then
	echo "transfer file:"$src" failed"
  echo
else
	echo "transfer file:"$src" sucessfuly"
  echo
fi
