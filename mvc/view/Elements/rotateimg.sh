for i in {1..359}
do
	ffmpeg -i 0.png -vf "rotate=$i*PI/180:c=none" imgs/$i.png	
done
