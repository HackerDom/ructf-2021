protoc --proto_path ../app/protobuf request.proto --js_out=import_style=commonjs,binary:../app/js
cd ../app/js && browserify request_pb.js main.js -o ../../public/js/bundle.js
