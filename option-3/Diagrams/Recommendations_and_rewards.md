# Recommendations and rewards

**Eliott leads the student pages and recommendations. William handles saved progress. Rick pairs on model training.**

We help students find useful practice. Badges and points follow rules we can explain. Machine learning helps choose exercises.

## Start with a helpful rule

After three unsuccessful attempts at the same exercise, offer an easier exercise in that topic. The student can accept or keep trying. An offer does not remove an earned level.

Exclude service failures and confirmed broken exercises. A syntax mistake should not be treated as proof that the student has forgotten an entire topic.

This rule works while we collect enough data. It is not the machine-learning module by itself.

## Then learn from results

Use exercise topic and difficulty together with earlier student results: topic progress, success rate, attempts, and recent activity. Keep time as a supporting signal because a student may leave a tab open.

A small Python model can learn which exercises students are likely to complete. The backend first removes disabled, unsuitable, or already completed candidates. The model helps rank the remaining choices. We aim for useful practice, not just the easiest exercise.

A reasonable first model is logistic regression through scikit-learn: it learns from labelled outcomes and estimates a probability. This is a proposal to test with our data, not a fixed requirement. [scikit-learn reference](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

Train on features known **before** the attempt; its later outcome is the label. Never give the model the answer it is meant to predict. Record the model version and measure on later, separate attempts before replacing a working model. Do not present invented activity as real student evidence.

With little data or a failed model, show ordinary topic/level recommendations. Retrain in batches as useful results grow. Keep a record of whether personalized recommendations actually improve on that starting rule.

## Ratings

A thumbs-up or thumbs-down describes the exercise's usefulness. A report describes a possible problem. Store them separately.

Ratings help both recommendation ranking and RAG example selection. Use the negative-vote percentage together with a minimum number of votes. Exact thresholds remain open. We should not hide a new exercise because its first rating was negative.

## Rewards

| Feature | Simple first idea |
| --- | --- |
| Badges | First completion, a topic milestone, or consistent practice |
| Levels | Saved progress separately for each topic |
| Leaderboard | Compare earned points; optionally filter by topic |

Show the reward and explain how it was earned. Save it so it remains after logout. Repeating a passed exercise is practice, not unlimited new points. Points, badge thresholds, and level boundaries are still to be chosen.

Shorter code, speed, and commit counts do not prove better understanding. We have no Git integration in the first version. We record submissions, not commits.

## Connections and routes

Correction → saved outcomes → recommendation features → Python model → suggested exercise IDs → student page.

Correction also updates completions → topic progress → badge rules and leaderboard. These reward rules do not require the ML model.

Routes: `GET /api/v1/recommendations`, `GET /api/v1/progress`, `GET /api/v1/activity`, `GET /api/v1/badges`, and `GET /api/v1/leaderboard`.

The subject's ML module requires personalized recommendations using behaviour and improvement over time (2 points, p.15). Badges, levels, and leaderboard cover three gamification mechanisms only when saved, explained, and shown to students (1 point, p.18).

[System diagram](05-recommendations-and-rewards.mmd)
