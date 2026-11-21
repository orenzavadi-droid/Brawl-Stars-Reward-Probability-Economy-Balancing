# לשינון ב-3 דקות — Brawl Stars Reward Probability & Economy Balancing

## המשפט היחיד שצריך לזכור

**אותו ערך צפוי לא מבטיח אותה חוויית שחקן.**

## סיפור הפרויקט ב-4 צעדים

1. **בעיה:** האם כדאי להכפיל את הסיכוי ל-Legendary?
2. **שיטה:** לקחתי את הסתברויות ה-Starr Drops הרשמיות ובניתי חלופה *היפותטית*. נתתי לכל נדירות ערך דמיוני אחיד כדי להחזיק **Expected Value = 108** בשתי החלופות.
3. **תוצאה:** הסיכוי ללפחות Legendary אחד ב-10 פתיחות עולה מ-**18.3% ל-33.5%**, אבל הסיכוי שחמש הפתיחות הראשונות כולן Rare עולה מ-**3.1% ל-23.7%**. גם חציון השווי של עשר פתיחות יורד מ-**950 ל-800 יחידות דמיוניות**.
4. **החלטה:** לא הייתי משיק מהסימולציה. הייתי בודק איזו חוויה אנחנו רוצים, נותן לשחקנים לנסות, ובודק תגובות אמיתיות ומדדי כלכלה.

## 45-second interview pitch (English)

"I took Supercell's published Starr Drop rarity odds and asked a Game Economist question: should we double the Legendary drop rate if the overall expected reward budget stays constant? I built a small counterfactual with invented reward values, so both designs cost 108 illustrative units per drop. The jackpot-heavy version raises the chance of seeing a Legendary in ten drops from 18 to 34 percent, but it also raises the chance that the first five drops are all Rare from 3 to 24 percent. So the math shows a tension between jackpot moments and frequent low-tier outcomes. I wouldn't claim that players actually feel worse or better without a playtest and a controlled experiment. That's the value of the project: translating player-experience intent into probability rules, economy constraints, and a testable decision."

## שלושה מושגים בלבד

- **Expected Value (EV)** — ממוצע הערך לאורך הרבה פתיחות: Σ(הסתברות × ערך). במקרה שלנו 108 *יחידות המחשה* בשתי החלופות.
- **Distribution / Variance** — איך פרסים מפוזרים סביב הממוצע. אותו ממוצע יכול להסתיר יותר קיצוניות.
- **Behavioral hypothesis** — השערה על איך השחקן *יחווה* את התגמולים. הסימולציה **לא מוכיחה** את הרגש.

## 3 שאלות קשות ותשובות קצרות

**האם זו הכלכלה האמיתית של Brawl Stars?** לא. רק הסתברויות הנדירות של A נלקחו מפרסום רשמי. כל ערכי התגמולים וחלופה B הומצאו להדגמה.

**למה זה פסיכולוגי?** כי אני בוחר הסתברויות מתוך כוונה חווייתית: האם המשחק אמור לתת תגמול צפוי או רגעי שיא נדירים? ואז אני בוחן את הפער בין הכוונה לדפוסי התגמול.

**למה לא פשוט לבחור את B?** כי יותר Legendary לא שווה בהכרח חוויה טובה יותר. צריך לבדוק שחקנים אמיתיים, סגמנטים והשלכות כלכליות לטווח הארוך.

## המלצה לתצוגה בראיון

פתח את `reports/interactive_case.html`: הצג **108 מול 108**, **18% מול 34%**, **3% מול 24%**. סיים ב-**"Same budget, different experience risk."**
