import 'dart:async';

import 'package:email_password_login/views/home_screen.dart';
import 'package:email_password_login/views/login_screen.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class VerifyScreen extends StatefulWidget {
  const VerifyScreen({ Key? key }) : super(key: key);

  @override
  _VerifyScreenState createState() => _VerifyScreenState();
}

class _VerifyScreenState extends State<VerifyScreen> {
  final _auth = FirebaseAuth.instance;
  late User user;
  late Timer timer;

  @override
  void initState() {
    user = _auth.currentUser!;
    user.sendEmailVerification();

    timer = Timer.periodic(Duration(seconds: 3), (timer){
      checkEmailVerified();
    });
    super.initState();
  }

  @override
  void dispose() {
    timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(child: Text('An email was sent to ${user.email},\n please verify'),),
    );
  }

  Future<void> checkEmailVerified() async{
    user = _auth.currentUser!;
    await user.reload();
    if (user.emailVerified){
      timer.cancel();
      Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (context) => LoginScreen()));
    }
  }
}