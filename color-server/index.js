var express = require('express');
const fileUpload = require('express-fileupload');
const shell = require('shelljs');
var app = express();

var shellcommand = ["cd .. && python3 colorization/colorize.py -img_in color-server/uploads/", " -img_out color-server/downloads/"]

var conversion = function(file_in){
	var file_out = file_in.split(".")[0] + "_1." + file_in.split(".")[1];
	var command = shellcommand[0] + file_in + shellcommand[1] + file_out;
	shell.exec(command, {silent: true}).stdout;
	return file_out;
}

app.use(fileUpload({
	limits: { fileSize: 50 * 1024 * 1024 },
}));

app.get('/', function(req, res){
	console.log("GET Request received");
	res.sendFile('index.html', { root: __dirname });
});

app.post('/upload', function(req, res){
	console.log("POST Request received");
	if (!req.files)
		return res.status(400).send('No files were uploaded');

	let videoFile = req.files.videoFile;
	let imageFile = req.files.imageFile;
	if (videoFile){
		var fname = videoFile.name;
		videoFile.mv(__dirname + '/uploads/' + fname, function(err){
			if (err)
				return res.status(500).send(err);
			res.send('File ' + fname + ' uploaded!');
		});
	}
	else if(imageFile){
		var fname = imageFile.name;
		imageFile.mv(__dirname + '/uploads/' + fname, function(err){
			if (err)
				return res.status(500).send(err);
			var file_out = conversion(fname);
			res.download(__dirname + '/downloads/' + file_out, file_out);
			//res.send('File ' + fname + ' uploaded!');
		});	
	}
	else{
		return res.status(400).send('No compatible files were uploaded');		
	}
});

app.listen(3000, () => console.log('Example app listening on port 3000!'))