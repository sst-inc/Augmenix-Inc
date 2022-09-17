import 'package:flutter/material.dart';
import 'package:percent_indicator/linear_percent_indicator.dart';
import 'package:scouts_flutter/badges.dart';
import 'package:scouts_flutter/journey.dart';
import 'package:scouts_flutter/main.dart';
import 'package:scouts_flutter/unit.dart';

import 'login.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  var tabid = 0;
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final signInBtnColorScheme = ColorScheme.fromSeed(
        seedColor: const Color.fromARGB(255, 226, 209, 15),
        brightness: theme.brightness);
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
                    tabid == 0
                        ? null
                        : Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const Home()),
                          );
                  },
                  child: Text(
                    "HOME",
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ),
                TextButton(
                  onPressed: () {
                    tabid == 1
                        ? null
                        : Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const Unit()),
                          );
                  },
                  child: Text(
                    "UNIT",
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ),
                TextButton(
                  onPressed: () {
                    tabid == 2
                        ? null
                        : Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const Badges()),
                          );
                  },
                  child: Text(
                    "BADGES",
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ),
                TextButton(
                  onPressed: () {
                    tabid == 3
                        ? null
                        : Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const Journey()),
                          );
                  },
                  child: Text(
                    "JOURNEY",
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ),
                const Spacer(),
                ElevatedButton(
                  onPressed: () async {
                    await googleSignIn.signOut();
                    Navigator.pushAndRemoveUntil(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const Login(),
                        ),
                        (route) => false);
                  },
                  style: ButtonStyle(
                    elevation: MaterialStateProperty.all(0),
                    backgroundColor:
                        MaterialStateProperty.all(Colors.transparent),
                    overlayColor: MaterialStateProperty.resolveWith((states) {
                      if (states.contains(MaterialState.hovered)) {
                        return signInBtnColorScheme.primaryContainer
                            .withOpacity(0.08);
                      } else if (states.contains(MaterialState.focused) ||
                          states.contains(MaterialState.pressed)) {
                        return signInBtnColorScheme.primaryContainer
                            .withOpacity(0.12);
                      }
                      return Colors.transparent;
                    }),
                    shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                      RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                        side: BorderSide(
                            color: signInBtnColorScheme.primary, width: 2),
                      ),
                    ),
                  ),
                  child: Text(
                    "SIGN OUT",
                    style: TextStyle(
                      color: signInBtnColorScheme.primary,
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Menu Bar Ends Here
          Expanded(
            child: Container(
              padding: const EdgeInsets.only(top: 50),
              child: Column(
                children: [
                  Text(
                    userPerson!.name,
                    style: Theme.of(context)
                        .textTheme
                        .displayLarge!
                        .copyWith(color: Theme.of(context).colorScheme.primary),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    "SST Fearless Falcons Unit, Patrol ${userPerson!.patrol}",
                    style: Theme.of(context)
                        .textTheme
                        .headlineSmall!
                        .copyWith(color: Theme.of(context).colorScheme.primary),
                  ),
                  const SizedBox(height: 50),
                  //Badges
                  Text(
                    "ACHIEVEMENTS (TBC) ",
                    style: Theme.of(context)
                        .textTheme
                        .headlineSmall!
                        .copyWith(color: Theme.of(context).colorScheme.primary),
                  ),
                  const SizedBox(height: 25),
                  Expanded(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Expanded(
                          child: GridView.builder(
                            itemCount: 3,
                            gridDelegate:
                                const SliverGridDelegateWithMaxCrossAxisExtent(
                              crossAxisSpacing: 20,
                              mainAxisSpacing: 20,
                              mainAxisExtent: 150,
                              maxCrossAxisExtent: 500,
                            ),
                            itemBuilder: (context, index) {
                              final achievements = userPerson!.progress;
                              return Container(
                                padding: const EdgeInsets.all(10),
                                child: Card(
                                  child: Row(
                                    children: [
                                      const SizedBox(width: 10),
                                      Padding(
                                        padding: const EdgeInsets.all(10),
                                        child: Image.asset(
                                            'assets/patrol/zetta.gif'), // TODO: Replace with actual image
                                      ),
                                      const SizedBox(width: 20),
                                      Column(
                                        children: [
                                          const SizedBox(height: 20),
                                          Text(achievements[index].badgeName),
                                          const SizedBox(height: 20),
                                          Text(achievements[index]
                                              .dateCompletion),
                                          const SizedBox(height: 20),
                                        ],
                                      ),
                                      const SizedBox(width: 10),
                                    ],
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 50),
                  // BADGES
                  Text(
                    "BADGES (TBC) ",
                    style: Theme.of(context)
                        .textTheme
                        .titleLarge!
                        .copyWith(color: Theme.of(context).colorScheme.primary),
                  ),
                  const SizedBox(height: 25),
                  Expanded(
                    child: GridView.builder(
                      itemCount: 2,
                      gridDelegate:
                          const SliverGridDelegateWithMaxCrossAxisExtent(
                        crossAxisSpacing: 20,
                        mainAxisSpacing: 40,
                        mainAxisExtent: 150,
                        maxCrossAxisExtent: 1000,
                      ),
                      itemBuilder: (context, index) {
                        final progress = userPerson!.progress;
                        return Container(
                          padding: const EdgeInsets.all(10),
                          child: Card(
                            child: Row(
                              children: [
                                Image.asset('assets/patrol/zetta.gif'),
                                Column(
                                  children: [
                                    Text(
                                      progress[index].badgeName,
                                      style: const TextStyle(
                                          fontSize: 24,
                                          fontWeight: FontWeight.bold),
                                    ),
                                    Text(progress[index].dateCompletion),
                                    LinearPercentIndicator(
                                      width: 500.0,
                                      lineHeight: 14.0,
                                      animation: true,
                                      animationDuration: 2000,
                                      percent: 0.5,
                                      barRadius: const Radius.circular(20),
                                      backgroundColor: Colors.grey,
                                      progressColor: Colors.green,
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
