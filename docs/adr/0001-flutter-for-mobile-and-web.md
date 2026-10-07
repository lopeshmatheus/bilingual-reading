# Flutter for mobile and web, like Linga

We build one Flutter (Dart) codebase for iOS, Android and the web, because the reading feel we want to match is Linga's, and Linga ships exactly this setup (app.linga.io serves Flutter's web bootstrap, and one codebase covers web, iOS, Android and desktop). Mobile and desktop get different reading layouts from the same code.

## Considered Options

- **Expo (React Native) + Next.js** gives real HTML text on the web (native selection, browser translate, hover), but means two UI codebases and less polish on the phone.
- **Fully native** (LingQ's approach: Swift, Android and a separate web app) needs three teams.

## Consequences

Flutter web paints text on a canvas, so browser text selection, the browser's own translate and find-in-page are weaker than on a normal web page. We accept that because selection, Glosses and Reveals are our own gestures anyway.
