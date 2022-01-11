import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class Loading extends StatefulWidget {

  @override
  _LoadingState createState() => _LoadingState();
}

class _LoadingState extends State<Loading> {

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    toNext();
  }

  toNext() async {
    await Future.delayed(Duration(milliseconds: 3500), () {});
    Navigator.pushReplacementNamed(context, '/home');
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[900],
      body: Center(
        child: SpinKitFoldingCube(
            color: Colors.white38,
        ),
      ),
    );
  }
}
