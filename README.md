由于上传github有文件夹大小限制，所以我删除了一些权重文件和图片视频。
1.删除了database文件夹下一个名为database.db的文件。
2.demo下output_frames下的语义分割图被我删除了。
3.model/dlib_model下删除了dlib_face_recognition_resnet_model_v1.dat和shape_predictor_68_face_landmarks.dat
4.我删除了mv下的视频。
5.pic下的图片也删除了。
6.out.mp4也删除了。

原始的部分文件结构
demonstration-system
├── database
│   └── database.db
├── demo
│   └── output_frames
│       └── 语义分割图
├── model
│   └── dlib_model
│       ├── dlib_face_recognition_resnet_model_v1.dat
│       └── shape_predictor_68_face_landmarks.dat
├── mv
│   └── 视频文件
├── pic
│   └── 图片文件
└── out.mp4

删除后对应的文件结构
demonstration-system
├── database
├── demo
│   └── output_frames
├── model
│   └── dlib_model
├── mv
├── pic
