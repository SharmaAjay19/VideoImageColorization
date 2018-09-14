git clone https://github.com/SharmaAjay19/VideoImageColorization.git
mv /home/ajsharm/VideoImageColorization /home/ajsharm/colorization
yes | sudo apt install caffe-cpu
yes | sudo apt install nodejs
yes | sudo apt install npm
cd colorization
./models/fetch_release_models.sh
cd color-server
mkdir downloads
mkdir uploads
npm install
node index.js

