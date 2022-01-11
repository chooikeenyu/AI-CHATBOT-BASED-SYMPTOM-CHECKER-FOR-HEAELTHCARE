import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:email_password_login/model/user_model.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:email_password_login/views/mentalmodel.dart';
import 'package:flutter/services.dart' as rootBundle;

import 'login_screen.dart';

String selectedCategory = 'Mental';
String selectedDisease = '';

class Homepage extends StatefulWidget {
  @override
  _HomepageState createState() => _HomepageState();
}
class _HomepageState extends State<Homepage> {

  List<String> categories = ["Mental", "Cancer", "Virus"];
  List<String> cancers = ["Lung Cancer", "Breast Cancer", "Kidney Cancer", "Leukemia Cancer", "Pancreatic Cancer"];
  List<String> mentals = ["Anxiety Disorders", "Mood Disorders", "Psychotic Disorders", "OC Disorders", "PTS Disorders"];
  List<String> viruses = ["Malaria Virus", "Dengue Virus", "COVID-19 Virus"];

  User? user = FirebaseAuth.instance.currentUser;
  UserModel loggedInUser = UserModel();

  @override
  void initState() {
    super.initState();
    FirebaseFirestore.instance
        .collection("users")
        .doc(user!.uid)
        .get()
        .then((value) {
      this.loggedInUser = UserModel.fromMap(value.data());
      setState(() {});
    });
  }

  Icon icon = new Icon(
    Icons.search,
    color: Colors.white,
  );

  final globalKey = new GlobalKey<ScaffoldState>();
  final TextEditingController _controller = new TextEditingController();
  List<dynamic> _list = [];
  bool _isSearching = true;
  String searchText = "";
  List searchresult = [];

  _HomepageState() {
    _controller.addListener(() {
      if (_controller.text.isEmpty) {
        setState(() {
          _isSearching = false;
          searchText = "";
        });
      } else {
        setState(() {
          _isSearching = true;
          searchText = _controller.text;
        });
      }
    });
  }

  void values() {
    _list = [];
    _list.add("Cancer");
    _list.add("Mental");
    _list.add("Dental");
    _list.add("Surgery");
    _list.add("Virus");
    _list.add("Infection");
    _list.add("Lung Cancer");
    _list.add("Breast Cancer");
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(colors: [Colors.deepPurple, Colors.lightBlueAccent]),
          ),
        ),
        title: Text(
          'MyHealthCare',
          style: TextStyle(
            fontFamily: 'Yuji',
            fontSize: 30.0,
          ),
        ),
        leading: Builder(builder: (context) =>
            IconButton(
                onPressed: () => Scaffold.of(context).openDrawer(),
                icon: Icon(Icons.menu)
            ),
        )
      ),
      body: Container(
        constraints: BoxConstraints.expand(),
        decoration: BoxDecoration(
            image: DecorationImage(
              image: AssetImage("assets/background.jpg"),
              fit: BoxFit.cover,
            )
        ),
        padding: EdgeInsets.symmetric(vertical: 5.0, horizontal: 20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 30.0),
            Container(
              child: Text('Hi, ${loggedInUser.firstName} ${loggedInUser.secondName} !',
                style: TextStyle(
                  fontFamily: 'BreeSerif',
                  color: Colors.black87,
                  fontSize: 20.0,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
            SizedBox(height: 40.0),
            Text('Find Healthcare Information Here',
              style: TextStyle(
                fontFamily: 'Sniglet',
                color: Colors.black87,
                fontSize: 20.0,
                fontWeight: FontWeight.w600,
              ),
            ),
            SizedBox(height: 15.0),
            Container(
              padding: EdgeInsets.symmetric(horizontal: 24.0),
              height: 40.0,
              decoration: BoxDecoration(
                color: Colors.grey.withOpacity(0.3),
                borderRadius: BorderRadius.circular(25.0),
              ),
              child: TextField(
                  decoration: InputDecoration(
                    helperStyle: TextStyle(color: Colors.black87),
                    contentPadding: EdgeInsets.symmetric(horizontal: 5.0, vertical: 13.0),
                    border: InputBorder.none,
                    icon: Icon(
                      Icons.search,
                      color: Colors.grey[600],
                    ),
                    hintText: 'Search',
                  ),
              ),
            ),
            SizedBox(height: 20.0),
            Text('Categories',
              style: TextStyle(
                fontFamily: 'Sniglet',
                color: Colors.black87.withOpacity(0.8),
                fontSize: 25.0,
                fontWeight: FontWeight.w600,
              ),
            ),
            SizedBox(height: 20.0),
            Flexible(
              child: Container(
                height: 50.0,
                child: ListView.builder(
                  itemCount: categories.length,
                  shrinkWrap: true,
                  physics: ClampingScrollPhysics(),
                  scrollDirection: Axis.horizontal,
                  itemBuilder: (context, index){
                    return CategoryTile(
                      category: categories[index],
                      isSelected: selectedCategory == categories[index],
                      context: this,
                    );
                  },
                ),
              ),
            ),
            SizedBox(height: 30.0),
            if (selectedCategory == 'Cancer')
              Flexible(
              child: Container(
                height: 200.0,
                child: ListView.builder(
                    itemCount: cancers.length,
                    shrinkWrap: true,
                    scrollDirection: Axis.horizontal,
                    itemBuilder: (context, index) {
                      return DiseaseTile(
                        disease: cancers[index],
                        isSelected: selectedDisease == cancers[index],
                        context: this,
                      );
                    }
                ),
              ),
              )
              else
                if(selectedCategory == 'Mental')
              Flexible(
                child: Container(
                  height: 200.0,
                  child: ListView.builder(
                      itemCount: mentals.length,
                      shrinkWrap: true,
                      scrollDirection: Axis.horizontal,
                      itemBuilder: (context, index){
                        return DiseaseTile(
                          disease: mentals[index],
                          isSelected: selectedDisease == mentals[index],
                          context: this,
                        );
                      }
                  ),
                ),
              ),
            if (selectedCategory == 'Virus')
              Flexible(
              child: Container(
                height: 200.0,
                child: ListView.builder(
                    itemCount: viruses.length,
                    shrinkWrap: true,
                    scrollDirection: Axis.horizontal,
                    itemBuilder: (context, index){
                      return DiseaseTile(
                        disease: viruses[index],
                        isSelected: selectedDisease == viruses[index],
                        context: this,
                      );
                    }
                ),
              ),
              ),
    ]
        ),
      ),
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                    colors: <Color>[
                      Colors.deepPurple,
                      Colors.lightBlue,
                    ],
                ),
              ),
              child: Container(
              child: Column(
                children: <Widget>[
                  Material(
                    borderRadius: BorderRadius.all(Radius.circular(60.0)),
                    elevation: 15.0,
                    child: Image.asset('assets/Logo.png', width: 105.0, height:105.0),
                  ),
                  Padding(padding: EdgeInsets.all(0.0)),
                  Text('MyHealthCare',style: TextStyle(fontFamily: 'Yuji', color: Colors.white, fontSize: 20.0)),
                ],
              ),
            ),
            ),
            CustomListTile(Icons.home,'Home',(){
              Navigator.pop(context, '/home');
            }),
            CustomListTile(Icons.person,'My Account',(){
              Navigator.pushNamed(context, '/account');
            }),
            CustomListTile(Icons.chat_bubble,'Chatbot',(){
              Navigator.pushNamed(context, '/chatbot');
            }),
            SizedBox(height: 285.0),
            CustomListTile(Icons.lock,'Logout',(){
              Navigator.pushNamed(context, '/');
            }),
          ],
        ),
      ),
    );
  }

    void _handleSearchStart() {
    setState(() {
    _isSearching = true;
    });
    }

    void _handleSearchEnd() {
      setState(() {
    this.icon = new Icon(
    Icons.search,
    color: Colors.white,
    );
    _isSearching = false;
    _controller.clear();
      });
    }

    void searchOperation(String searchText) {
    searchresult.clear();
    if (_isSearching != null) {
    for (int i = 0; i < _list.length; i++) {
    String data = _list[i];
    if (data.toLowerCase().contains(searchText.toLowerCase())) {
    searchresult.add(data);
             }
          }
       }
    }

}

class CustomListTile extends StatelessWidget {

  IconData icon;
  String text;
  VoidCallback onTap;
  CustomListTile(this.icon, this.text, this.onTap);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(8.0,0,8.0,0),
      child: Container(
        decoration: BoxDecoration(
          border: Border(bottom: BorderSide(color: Colors.grey.shade400)),
        ),
        child: InkWell(
          splashColor: Colors.blueAccent,
          onTap: onTap,
          child: Container(
            height: 50.0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: <Widget>[
                Row(
                  children: <Widget>[
                    Icon(icon),
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(text,style: TextStyle(
                        fontSize: 16.0,
                      ),
                      ),
                    ),
                  ],
                ),
                Icon(Icons.arrow_right),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class CategoryTile extends StatefulWidget {

  String category;
  bool isSelected;
  _HomepageState context;
  CategoryTile({this.category='', this.isSelected = true, required this.context});

  @override
  State<CategoryTile> createState() => _CategoryTileState();
}

class _CategoryTileState extends State<CategoryTile> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (){
        widget.context.setState(() {
          selectedCategory = widget.category;
        });
      },
      child: Container(
        alignment: Alignment.center,
        padding: EdgeInsets.symmetric(horizontal: 30.0, vertical: 0.0),
        margin: EdgeInsets.only(left: 10.0, right: 10.0),
        decoration: BoxDecoration(
          color: widget.isSelected ? Colors.blue[800] : Colors.grey[200],
          borderRadius: BorderRadius.circular(10.0),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5),
              spreadRadius: 3,
              blurRadius: 3,
              offset: Offset(5.2, 5), // changes position of shadow
            ),
          ],
        ),
        child: Text(widget.category,
        style: TextStyle(
          fontFamily: 'Comforta',
          color: widget.isSelected ? Colors.white : Colors.black,
        ),
        ),
      ),
    );
  }
}

class DiseaseTile extends StatefulWidget {

  String disease;
  String diseaseName;
  bool isSelected;
  _HomepageState context;
  DiseaseTile({this.disease = '', this.diseaseName = '', this.isSelected = true, required this.context});

  @override
  State<DiseaseTile> createState() => _DiseaseTileState();
}

class _DiseaseTileState extends State<DiseaseTile> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        widget.context.setState(() {
          selectedDisease = widget.disease;
          Navigator.push(context, MaterialPageRoute(builder: (context) => new Healthcare(diseaseName: selectedDisease)),
          );
        });
      },

      child: Container(
        alignment: Alignment.center,
        padding: EdgeInsets.symmetric(horizontal: 50.0),
        margin: EdgeInsets.only(left: 15.0, right: 15.0),
        decoration: BoxDecoration(
          color: widget.isSelected ? Colors.blue[800] : Colors.grey[200],
          borderRadius: BorderRadius.circular(10.0),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5),
              spreadRadius: 5,
              blurRadius: 7,
              offset: Offset(5.2, 5), // changes position of shadow
            ),
          ],
        ),
        child: Text(widget.disease,
          style: TextStyle(
            fontFamily: 'Comforta',
            fontSize: 15.0,
            color: widget.isSelected ? Colors.white : Colors.black,
          ),
        ),
      ),
    );
  }


  
}

class Healthcare extends StatefulWidget {
  const Healthcare({Key? key, required String diseaseName}) : super(key: key);

  @override
  State<Healthcare> createState() => _HealthcareState();
}


class _HealthcareState extends State<Healthcare> {
  List _Infos = [];
  int i = 0;
  String disName = selectedDisease;

  int WhatMental () {
    if (disName == 'Anxiety Disorders')
      i = 0;
    if (disName == 'Mood Disorders')
      i = 1;
    if (disName == 'Psychotic Disorders')
      i = 2;
    if (disName == 'OC Disorders')
      i = 3;
    if (disName == 'PTS Disorders')
      i = 4;
    return i;
  }

  int WhatCancer () {
    if (disName == 'Lung Cancer')
      i = 0;
    if (disName == 'Breast Cancer')
      i = 1;
    if (disName == 'Kidney Cancer')
      i = 2;
    if (disName == 'Leukemia Cancer')
      i = 3;
    if (disName == 'Pancreatic Cancer')
      i = 4;
    return i;
  }

  int WhatVirus() {
    if (disName == 'Malaria Virus')
      i = 0;
    if (disName == 'Dengue Virus')
      i = 1;
    if (disName == 'COVID-19 Virus')
      i = 2;

    return i;
  }


  Future<void> ReadJsonData() async {
    final String res = await rootBundle.rootBundle.loadString('jsonfile/mentals_data.json');
    final mentalsData = await json.decode(res);

    if (_Infos != null && _Infos.length > i) {
      _Infos[i];
    }

    if(disName.contains('Disorders')) {
      WhatMental();
      setState(() {
        _Infos = mentalsData["mentals"];
      });
    }
    if(disName.contains('Cancer')) {
      setState(() {
        _Infos = mentalsData["cancers"];
      });
      WhatCancer();
    }
    if(disName.contains('Virus')) {
      setState(() {
        _Infos = mentalsData["viruses"];
      });
      WhatVirus();
    }


  }

  @override
  Widget build(BuildContext context) {
    ReadJsonData();
    return Scaffold(
      appBar: AppBar(
        title: Text('Health Information'),
      ),
        body: Container(
          constraints: BoxConstraints.expand(),
          decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage("assets/background.jpg"),
                fit: BoxFit.cover,
              )
          ),
          child: SingleChildScrollView(
            physics: BouncingScrollPhysics(),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                Padding(
                    padding: EdgeInsets.symmetric(horizontal: 16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      SizedBox(height: 10.0),
                      Row(
                        children: [
                            Container(
                              width: 215.0,
                            child: Text(
                              _Infos[i]["name"],
                              style: TextStyle(
                                fontFamily: 'BreeSerif',
                              fontSize: 30.0,
                              fontWeight: FontWeight.bold,
                              color: Colors.black,
                              ),
                            ),
                          ),
                          SizedBox(width: 35.0),
                          ClipRRect(
                            borderRadius: BorderRadius.circular(60.0),
                            child: Material(
                              elevation: 15.0,
                            child: Image.asset(_Infos[i]["image"], height: 120.0, width: 120.0, fit: BoxFit.cover),
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 10.0),
                      Padding(
                        padding: EdgeInsets.only(bottom: 8),
                        child: Text(
                          _Infos[i]["what"],
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey[800],
                            fontFamily: 'Balsamiq',
                          ),
                        ),
                      ),
                      SizedBox(height: 5.0),
                      Padding(
                        padding: EdgeInsets.only(bottom: 8),
                        child: Text(
                          _Infos[i]["type"],
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey[800],
                            fontFamily: 'Balsamiq',
                          ),
                        ),
                      ),
                      SizedBox(height: 5.0),
                      Padding(
                        padding: EdgeInsets.only(bottom: 8),
                        child: Text(
                          _Infos[i]["causes"],
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey[800],
                            fontFamily: 'Balsamiq',
                          ),
                        ),
                      ),
                      SizedBox(height: 5.0),
                      Padding(
                        padding: EdgeInsets.only(bottom: 8),
                        child: Text(
                          _Infos[i]["symptoms"],
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey[800],
                            fontFamily: 'Balsamiq',
                          ),
                        ),
                      ),
                      SizedBox(height: 5.0),
                      Padding(
                        padding: EdgeInsets.only(bottom: 8),
                        child: Text(
                          _Infos[i]["treatment"],
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey[800],
                            fontFamily: 'Balsamiq',
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
    );
  }

  Future<void> logout(BuildContext context) async {
    await FirebaseAuth.instance.signOut();
    Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => LoginScreen()));
  }
}


