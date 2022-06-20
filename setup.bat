echo Installing pip packages
call .\venv\Scripts\activate.bat
pip install -r requirements.txt

@echo Syncing git submodules
git submodule update --init
git submodule status

@echo Copying over Tensorflow pre-processing scripts
copy submodules\models\research\object_detection\model_main_tf2.py training\tensorflow_scripts
copy submodules\models\research\object_detection\exporter_main_v2.py training\tensorflow_scripts
copy submodules\models\research\object_detection\export_tflite_graph_tf2.py training\tensorflow_scripts

deactivate