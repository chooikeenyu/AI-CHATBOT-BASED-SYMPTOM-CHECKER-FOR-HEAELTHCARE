import 'package:email_password_login/views/home_screen.dart';
import 'package:email_password_login/views/login_screen.dart';
import 'package:email_password_login/views/account.dart';
import 'package:email_password_login/views/chatbot.dart';
import 'package:email_password_login/views/home.dart';
import 'package:email_password_login/views/loading.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chatbot App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => LoginScreen(),
        '/loading': (context) => Loading(),
        '/home': (context) =>  Homepage(),
        '/account': (context) => MyAccount(),
        '/chatbot': (context) => Chatbot(),
      },
    );
  }
}