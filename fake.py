from flask import Flask,render_template_string,request,Response,jsonify
from PIL import Image
import os,cv2,insightface,numpy as np
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='.'
html='''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Deepfake Web App</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{height:100vh;font-family:Arial,sans-serif;background:linear-gradient(45deg,#667eea 0%,#764ba2 100%);display:flex;flex-direction:column;overflow:hidden;}
        header{text-align:center;padding:20px;font-size:2.5rem;font-weight:700;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,0.3);}
        .main{flex:1;display:flex;align-items:center;justify-content:center;position:relative;}
        .webcam-box{width:80vw;height:60vh;max-width:800px;max-height:600px;border-radius:20px;border:3px solid #fff;background:#000;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.3);}
        .webcam-box img{width:100%;height:100%;object-fit:cover;border-radius:17px;}
        .upload-area{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);background:rgba(255,255,255,0.95);border-radius:15px;padding:15px 20px;box-shadow:0 5px 20px rgba(0,0,0,0.2);border:2px solid #667eea;}
        #dropbox{width:150px;height:50px;border:2px dashed #667eea;border-radius:10px;display:flex;align-items:center;justify-content:center;cursor:pointer;background:#f8f9ff;transition:all 0.3s;font-size:14px;color:#667eea;font-weight:600;}
        #dropbox:hover{border-color:#764ba2;color:#764ba2;background:#fff;box-shadow:0 2px 10px rgba(118,75,162,0.2);}
        .success{color:#28a745;font-weight:600;margin-top:8px;font-size:13px;text-align:center;}
        @media(max-width:768px){
            .webcam-box{width:95vw;height:50vh;}
            header{font-size:2rem;padding:15px;}
            .upload-area{bottom:20px;padding:12px 15px;}
            #dropbox{width:120px;height:45px;font-size:12px;}
        }
    </style>
</head>
<body>
    <header>Deepfake Web App</header>
    <div class="main">
        <div class="webcam-box">
            <img id="webcam" src="/video_feed" alt="Webcam Stream"/>
        </div>
        <div class="upload-area">
            <form id="uploadForm" method=post enctype=multipart/form-data>
                <div id="dropbox">Upload Image</div>
                <input type=file name=file accept="image/*" onchange="uploadImage(this.files[0])" style="display:none" id="fileInput">
                <div id="successMsg">{% if uploaded %}<div class="success">Image uploaded!</div>{% endif %}</div>
            </form>
        </div>
    </div>
    <script>
        const dropbox=document.getElementById('dropbox');
        dropbox.onclick=()=>document.getElementById('fileInput').click();
        dropbox.ondragover=e=>{e.preventDefault();dropbox.style.borderColor='#764ba2';};
        dropbox.ondragleave=e=>{e.preventDefault();dropbox.style.borderColor='#667eea';};
        dropbox.ondrop=e=>{
            e.preventDefault();
            dropbox.style.borderColor='#667eea';
            const dt=e.dataTransfer;
            if(dt.files.length){uploadImage(dt.files[0]);}
        };
        function uploadImage(file){
            const formData=new FormData();
            formData.append('file',file);
            fetch('/',{method:'POST',body:formData})
            .then(response=>response.json())
            .then(data=>{
                if(data.no_face){
                    alert('No face detected in the uploaded image. Please try another image.');
                }else{
                    document.getElementById('successMsg').innerHTML='<div class="success">Image uploaded!</div>';
                    setTimeout(()=>{location.reload();},500);
                }
            });
        }
        document.addEventListener('keydown',function(e){
            if(e.key==='Escape'){location.reload();}
        });
    </script>
</body>
</html>'''
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        if 'file' not in request.files: return jsonify({'no_face':True})
        file=request.files['file']
        if file.filename=='': return jsonify({'no_face':True})
        if file: img=Image.open(file.stream).convert('RGB')
        img.save(os.path.join(app.config['UPLOAD_FOLDER'],'source.png'))
        source_img=cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'],'source.png'))
        face_analyzer=insightface.app.FaceAnalysis(name='buffalo_l')
        face_analyzer.prepare(ctx_id=0,det_size=(640,640))
        source_faces=face_analyzer.get(source_img)
        if not source_faces:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],'source.png'))
            return jsonify({'no_face':True})
        return jsonify({'no_face':False})
    return render_template_string(html,uploaded=False)
def gen_deepfake():
    source_path=os.path.join(app.config['UPLOAD_FOLDER'],'source.png')
    if not os.path.exists(source_path):
        blank=np.zeros((600,800,3),dtype=np.uint8)
        _,jpeg=cv2.imencode('.jpg',blank)
        while True: yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n')
    else:
        source_img=cv2.imread(source_path)
        if source_img is None: source_img=np.zeros((600,800,3),dtype=np.uint8)
        face_analyzer=insightface.app.FaceAnalysis(name='buffalo_l')
        face_analyzer.prepare(ctx_id=0,det_size=(640,640))
        swapper=insightface.model_zoo.get_model('inswapper_128.onnx',download=True)
        source_faces=face_analyzer.get(source_img)
        if not source_faces: source_face=None
        else: source_face=source_faces[0]
        cam=cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH,800)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
        frame_count=0
        last_result=None
        scale=0.2
        while True:
            ret,frame=cam.read()
            if not ret:break
            frame=cv2.resize(frame,(800,600))
            frame_count+=1
            if source_face is not None and frame_count%5==0:
                small_frame=cv2.resize(frame,(0,0),fx=scale,fy=scale)
                target_faces=face_analyzer.get(small_frame)
                result=frame.copy()
                for target_face in target_faces:
                    target_face.bbox=[int(x/scale) for x in target_face.bbox]
                    if hasattr(target_face,'kps'):
                        target_face.kps=np.array([[x/scale,y/scale] for x,y in target_face.kps])
                    result=swapper.get(result,target_face,source_face,paste_back=True)
                last_result=result
            else:
                result=last_result if last_result is not None else frame
            _,jpeg=cv2.imencode('.jpg',result)
            yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'+jpeg.tobytes()+b'\r\n')
        cam.release
@app.route('/video_feed')
def video_feed():
    return Response(gen_deepfake(),mimetype='multipart/x-mixed-replace;boundary=frame')
if __name__=='__main__':
    app.run()
    