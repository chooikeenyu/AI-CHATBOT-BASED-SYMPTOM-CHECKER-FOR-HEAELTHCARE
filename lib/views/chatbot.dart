import 'dart:convert';

import 'package:bubble/bubble.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;


class Chatbot extends StatefulWidget {
  const Chatbot({Key? key}) : super(key: key);

  @override
  _ChatbotState createState() => _ChatbotState();
}

class _ChatbotState extends State<Chatbot> {
  // final Map<String, HighlightedWord> _highlights = {
  //   'flutter': HighlightedWord(
  //     onTap: () => print('flutter'),
  //     textStyle: const TextStyle(
  //       color: Colors.blue,
  //       fontWeight: FontWeight.bold,
  //     ),
  //   ),
  // };

  // late stt.SpeechToText _speech;
  // bool _isListening = false;
  // String _text = 'Press the button and start speaking';
  // double _confidence = 1.0;

  final GlobalKey<AnimatedListState> _listKey = GlobalKey();
  List<String> _data = [];
  static const String BOT_URL = "http://10.0.2.2:5000/bot";
  TextEditingController queryController = TextEditingController();

  // @override
  // void initState() {
  //   super.initState();
  //   _speech = stt.SpeechToText();
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],
      appBar: AppBar(
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(colors: [Colors.deepPurple, Colors.lightBlueAccent]),
          ),
        ),
        centerTitle: true,
        title: Text('MyHealthcare Agent',
        style: TextStyle(
            fontFamily: 'BreeSerif',
        ),
        ),
      ),
      // floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      // floatingActionButton: AvatarGlow(
      //   animate: _isListening,
      //   glowColor: Theme.of(context).primaryColor,
      //   endRadius: 75.0,
      //   duration: const Duration(milliseconds: 2000),
      //   repeatPauseDuration: const Duration(milliseconds: 100),
      //   repeat: true,
      //   child: FloatingActionButton(
      //     onPressed: _listen,
      //     child: Icon(_isListening ? Icons.mic : Icons.mic_none),
      //   ),
      // ),
      body: Stack(
        children: <Widget>[
          Container(
      decoration: BoxDecoration(
          image: DecorationImage(
          image: AssetImage("assets/background.jpg"),
      fit: BoxFit.cover,
    )
    ),
            child: AnimatedList(
              padding: EdgeInsets.only(bottom: 70.0),
              key: _listKey,
              initialItemCount: _data.length,
              physics: BouncingScrollPhysics(),
              itemBuilder:
                  (BuildContext context, int index, Animation animation) {
                return buildItem(_data[index], index, animation);
              },
            ),
          ),

          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Align(
              alignment: Alignment.bottomCenter,
              child: ColorFiltered(
                colorFilter: ColorFilter.linearToSrgbGamma(),
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    color: Colors.white,
                  ),
                  // color: Colors.white,
                  child: Row(
                    children: <Widget>[
                      Flexible(
                          child: Padding(
                            padding: const EdgeInsets.all(3.0),
                            child: TextField(
                              enableInteractiveSelection: true,
                                style: TextStyle(
                                    color: Colors.black,
                                        fontFamily: 'Balsamiq',
                                ),
                                controller: queryController,
                                decoration: InputDecoration(
                                  icon: Icon(
                                    Icons.message,
                                    color: Colors.blue[800],
                                    size: 30.0,
                                  ),
                                  hintText: "Send your message!",
                                  hintStyle: TextStyle(
                                      fontWeight: FontWeight.w400,
                                      color: Colors.grey,
                                    fontFamily: 'Balsamiq',
                                  ),
                                )
                            ),
                          )
                      ),
                      Container(
                        margin: EdgeInsets.symmetric(horizontal: 4.0),
                        child: IconButton(
                          icon: Icon(
                            Icons.send,
                            size: 30.0,
                            color: Colors.blue[800],
                          ),
                          onPressed: () {
                            this.getResponse();
                          },
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
  //
  // void _listen() async {
  //   if (!_isListening) {
  //     bool available = await _speech.initialize(
  //       onStatus: (val) => print('onStatus: $val'),
  //       onError: (val) => print('onError: $val'),
  //     );
  //     if (available) {
  //       setState(() => _isListening = true);
  //       _speech.listen(
  //         onResult: (val) => setState(() {
  //           _text = val.recognizedWords;
  //           if (val.hasConfidenceRating && val.confidence > 0) {
  //             _confidence = val.confidence;
  //           }
  //         }),
  //       );
  //     }
  //   } else {
  //     setState(() => _isListening = false);
  //     _speech.stop();
  //   }
  // }

  void getResponse() {
    if (queryController.text.length > 0) {
      this.insertSingleItem(queryController.text);
      var client = http.Client();
      try {
        client.post(Uri.parse(BOT_URL),
            body: {"query": queryController.text}).then((response) {
          print(response.body);
          print(response.statusCode);
          Map<String, dynamic> data = jsonDecode(response.body);
          insertSingleItem(data['response'] + "<bot>");
        });
      } catch (e) {
        print("Failed -> $e");
      } finally {
        client.close();
        queryController.clear();
      }
    }
  }

  void insertSingleItem(String message) {
    _data.add(message);
    _listKey.currentState!.insertItem(_data.length - 1);
  }

// get client

// http.Client getClient(){
//   return http.Client();
// }

}

Widget buildItem(String item, int index, animation) {
  bool mine = item.endsWith("<bot>");
  return SizeTransition(
    sizeFactor: animation,
    child: Padding(
      padding: EdgeInsets.only(left: 14,right: 14,top: 10,bottom: 10),
      child: Container(
        alignment: mine ? Alignment.topLeft : Alignment.topRight,
        child: Bubble(
          child: Text(
            item.replaceAll("<bot", ""),
            style: TextStyle(
                color: mine ? Colors.white : Colors.black,
              fontFamily: 'Balsamiq'
            ),
          ),
          color: mine ? Colors.blue[800] : Colors.grey[200],
          padding: BubbleEdges.all(12.5),
        ),
      ),
    ),
  );
}

