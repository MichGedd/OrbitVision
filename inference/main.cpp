#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>
#include <tensorflow/lite/optional_debug_tools.h>

#include <string>

#include <edgetpu.h>

using namespace std;
using namespace cv;
using namespace std::chrono;

int main() {
	Mat frame;
	Mat framePreProcess;

	const auto &tpus = edgetpu::EdgeTpuManager::GetSingleton()->EnumerateEdgeTpu();

	if(tpus.size() < 1) {
		std::cerr << "Can't find edgetpu\n";
		std::abort;
	}

	//unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile("../inference/model_320x320.tflite");
	cout << "Start of program" << endl;
	unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile("../inference/FRC_2022_nofpn_edgetpu.tflite"); // Make sure paths are correct
	cout << "Found model" << endl;
	shared_ptr<edgetpu::EdgeTpuContext> edgetpu_context = edgetpu::EdgeTpuManager::GetSingleton()->OpenDevice(); // New

	int id = 0;
	for(const auto &tpu : tpus) {
		cout << "\ntype: " << tpu.type << "\npath: " << tpu.path << "\n";
	}

	cout << "Opened edgetpu" << endl;
	tflite::ops::builtin::BuiltinOpResolver resolver;
	resolver.AddCustom(edgetpu::kCustomOp, edgetpu::RegisterCustomOp());  // New
	cout << "Added custom ops" << endl;
	//tflite::InterpreterBuilder builder(*model, resolver);
	unique_ptr<tflite::Interpreter> interpreter;
	//builder(&interpreter);

	if(tflite::InterpreterBuilder(*model, resolver)(&interpreter) != kTfLiteOk) {
		cout << "Failed to build interpreter" << endl;
		exit(1);
	}

	cout << "Built interpreter" << endl;

	interpreter->SetExternalContext(kTfLiteEdgeTpuContext, edgetpu_context.get()); // New
	cout << "Set external context" << endl;
	interpreter->SetNumThreads(1);  // New
	cout << "Set threads" << endl;

	// interpreter->SetNumThreads(4);
	// interpreter->AllocateTensors();

	if(interpreter->AllocateTensors() != kTfLiteOk) {
		cout << "Failed to allocate tensors" << endl;
		exit(1);
	}

	cout << "Allocated tensors" << endl;
	tflite::PrintInterpreterState(interpreter.get());

	//float *inputLayer = interpreter->typed_input_tensor<float>(0);
	//float *output = interpreter->typed_output_tensor<float>(0);

	uint8_t *inputLayer = interpreter->typed_input_tensor<uint8_t>(0);
	uint8_t *scores = interpreter->typed_output_tensor<uint8_t>(0);
	uint8_t *boxes = interpreter->typed_output_tensor<uint8_t>(1);

	auto tensorValToPixel = [](uint8_t tensorVal) {
		// return (int)(((tensorVal * 0.00632279f) - 0.297684f) * 640);
		return (int)(((tensorVal * 0.0123466f) - 1.33652f) * 320);
	};

	VideoCapture cap;
	cap.open(0, CAP_V4L2);

	cout << "Opened camera" << endl;

	cap.set(CAP_PROP_FRAME_WIDTH, 320);
	cap.set(CAP_PROP_FRAME_HEIGHT, 320);

	cout << "Set camera properties" << endl;

	while(1) {

		auto start = system_clock::now();
		cap.read(frame);

		if(frame.empty()) {
			cout << "ERROR: EMPTY FRAME" << endl;
			continue;
		}

		int dimX = frame.rows;
		int dimY = frame.cols;

		if(dimX >= dimY) {
			int diff = dimX - dimY;
			copyMakeBorder(frame, framePreProcess, 0, diff, 0, 0, BORDER_CONSTANT, Scalar(0, 0, 0));
		} else if (dimY > dimX) {
			int diff = dimY - dimX;
			copyMakeBorder(frame, framePreProcess, 0, 0, 0, diff, BORDER_CONSTANT, Scalar(0, 0, 0));
		}
		// resize(framePreProcess, framePreProcess, Size(640, 640), INTER_AREA);
		resize(framePreProcess, framePreProcess, Size(300, 300), INTER_AREA);
		cvtColor(framePreProcess, framePreProcess, COLOR_BGR2RGB);
		//frame_pp.convertTo(input, CV_32FC3, (2.0 / 255.0), -1.0);

		//memcpy(inputLayer, input.ptr<float>(0), 640 * 640 * 3 * sizeof(float));
		memcpy(inputLayer, framePreProcess.ptr<uint8_t>(0), 300 * 300 * 3 * sizeof(uint8_t));

		interpreter->Invoke();

		for(int i = 0; i < 10; i++) {
			if(scores[i] / 255.0f >= 0.8) {
			// TODO: Cast to frame, not framePreProcess

			int yMin = tensorValToPixel(boxes[i * 4]);
			int xMin = tensorValToPixel(boxes[(i * 4) + 1]);
			int yMax = tensorValToPixel(boxes[(i * 4) + 2]);
			int xMax = tensorValToPixel(boxes[(i * 4) + 3]);

			rectangle(framePreProcess, Point(xMin, yMin), Point(xMax, yMax), Scalar(0, 255, 0));
			}
		}

		auto end = system_clock::now();
		auto ms = duration_cast<milliseconds>(end - start);
		cout << "Frame Time: " << ms.count() << endl;

		imshow("Live", framePreProcess);
		if(waitKey(5) >= 0) {
			break;
		}
	}

	return 0;
}
