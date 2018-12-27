for i in {1..10}
do
	convert -size `python -c "import random; print random.randint(500,1000)"`x`python -c "import random; print random.randint(500,1000)"` \
		xc:`python -c "import random; print \"#\"+\"\".join([random.choice(\"0123456789abcdef\") for j in range(6)])"` \
		-gravity center \
		-fill black \
		-weight 700 \
		-pointsize 200 \
		-annotate 0 "$i" "$i.jpg"
done
