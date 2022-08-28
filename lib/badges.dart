import 'package:flutter/material.dart';
import 'package:scouts_flutter/home.dart';
import 'package:scouts_flutter/main.dart';
import 'package:scouts_flutter/badges.dart';

class Badges extends StatefulWidget {
  const Badges({Key? key}) : super(key: key);

  @override
  State<Badges> createState() => _BadgesState();
}

class _BadgesState extends State<Badges> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Menu Bar -> Shift to a widgets so that it can be reused
          Container(
            color: Theme.of(context).colorScheme.primaryContainer,
            height: 50,
            padding: const EdgeInsets.only(left: 10),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset(
                  'assets/logo.jpg',
                  fit: BoxFit.cover,
                  height: 40,
                ),
                const Spacer(),
                TextButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: Text(
                    "UNIT",
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ),
                TextButton(
                  onPressed: () {},
                  child: Text(
                    "BADGES",
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ),
                TextButton(
                  onPressed: () {},
                  child: Text(
                    "MY SCOUTING JOURNEY",
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ),
                const Spacer(),
              ],
            ),
          ),
          // Menu Bar Ends Here
          Expanded(
            child: Container(
              padding: const EdgeInsets.only(top: 40),
              child: Column(
                children: [
                  Text(
                    "Badges",
                    style: Theme.of(context)
                        .textTheme
                        .displayLarge!
                        .copyWith(color: Theme.of(context).colorScheme.primary),
                  ),
                  const SizedBox(height: 20),
                  Expanded(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: (GridView.builder(
                        itemCount: userPerson!.progress.length,
                        gridDelegate:
                            const SliverGridDelegateWithMaxCrossAxisExtent(
                          crossAxisSpacing: 20,
                          mainAxisSpacing: 20,
                          mainAxisExtent: 200,
                          maxCrossAxisExtent: 200,
                        ),
                        itemBuilder: (context, index) {
                          final achievements = userPerson!.progress;
                          return Card(
                            child: Column(
                              children: [
                                Padding(
                                  padding: const EdgeInsets.all(10),
                                  child: Image.asset('assets/patrol/zetta.gif'),
                                ),
                                const SizedBox(height: 10),
                                Text(achievements[index].badgeName),
                                const SizedBox(height: 20),
                              ],
                            ),
                          );
                        },
                      )),
                    ),
                  ),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
