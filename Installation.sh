git clone https://github.com/SharmaAjay19/VideoImageColorization.git
mv /home/ajsharm/VideoImageColorization /home/ajsharm/colorization
sudo apt install caffe-cpu
sudo apt install nodejs
sudo apt install npm
cd colorization
./models/fetch_release_models.sh
cd color-server
mkdir downloads
mkdir uploads
npm install
node index.js
