from sqlalchemy.sql import text
from db import db
from services import users

def populate_database():
    sql = text("SELECT * FROM Users")
    result = db.session.execute(sql).fetchall()
    if len(result) > 1:
        return

    usernames = [
        'Alice', 'Bob', 'Charlie', 'David', 'Eva',
        'Frank', 'Grace', 'Henry', 'Ivy', 'Jack',
        'Kate', 'Leo', 'Mia', 'Noah', 'Olivia',
        'Peter', 'Quinn', 'Rachel', 'Sam', 'Taylor'
    ]
    for username in usernames:
        users.create_user(username, username)

    profile_query = text(
        """
        INSERT INTO profiles (id, user_id, bio, image_data) VALUES
        (1, 1, 'Language enthusiast exploring new horizons.', NULL),
        (2, 2, 'Lover of linguistics and cultural exchange.', NULL),
        (3, 3, 'Passionate about learning multiple languages.', NULL),
        (4, 4, 'Language learning is an exciting journey!', NULL),
        (5, 5, 'Dedicated to mastering languages for communication.', NULL),
        (6, 6, 'Learning languages broadens the mind.', NULL),
        (7, 7, 'Language learning is a lifelong adventure.', NULL),
        (8, 8, 'Embarking on a journey to fluency in various languages.', NULL),
        (9, 9, 'Exploring the world through language exploration.', NULL),
        (10, 10, 'Language learning is both challenging and rewarding.', NULL),
        (11, 11, 'Passionate about connecting through different languages.', NULL),
        (12, 12, 'Mastering languages opens doors to new opportunities.', NULL),
        (13, 13, 'Adventurous spirit with a love for diverse languages.', NULL),
        (14, 14, 'Curious language learner with a keen interest in cultures.', NULL),
        (15, 15, 'Passionate about language learning and cultural exchange.', NULL),
        (16, 16, 'Enthusiastic language learner aiming for fluency.', NULL),
        (17, 17, 'Language enthusiast seeking connections worldwide.', NULL),
        (18, 18, 'Dedicated to the pursuit of fluency in multiple languages.', NULL),
        (19, 19, 'Exploring the beauty of languages and global connections.', NULL),
        (20, 20, 'Adventurous language learner with a love for diversity.', NULL)
        """
    )
    db.session.execute(profile_query)
    db.session.commit()

    languages_query = text(
        """
        INSERT INTO language_levels (user_id, language_id, proficiency_level)
        VALUES
        (1, 1, 'Fluent'),
        (2, 2, 'Intermediate'),
        (3, 3, 'Beginner'),
        (4, 4, 'Fluent'),
        (5, 5, 'Intermediate'),
        (6, 6, 'Fluent'),
        (7, 7, 'Beginner'),
        (8, 8, 'Intermediate'),
        (9, 9, 'Fluent'),
        (10, 10, 'Fluent'),
        (11, 11, 'Intermediate'),
        (12, 12, 'Beginner'),
        (13, 13, 'Fluent'),
        (14, 14, 'Intermediate'),
        (15, 15, 'Fluent'),
        (16, 16, 'Beginner'),
        (17, 17, 'Fluent'),
        (18, 18, 'Intermediate'),
        (19, 19, 'Fluent'),
        (20, 20, 'Beginner'),
        (1, 7, 'Intermediate'),
        (2, 8, 'Fluent'),
        (3, 9, 'Beginner'),
        (4, 10, 'Intermediate'),
        (5, 11, 'Fluent'),
        (6, 12, 'Beginner'),
        (7, 13, 'Intermediate'),
        (8, 14, 'Fluent'),
        (9, 15, 'Beginner'),
        (10, 16, 'Intermediate'),
        (11, 18, 'Fluent'),
        (12, 20, 'Intermediate'),
        (13, 17, 'Fluent'),
        (14, 16, 'Beginner'),
        (15, 16, 'Intermediate'),
        (16, 14, 'Fluent'),
        (17, 13, 'Beginner'),
        (18, 12, 'Intermediate'),
        (19, 11, 'Fluent'),
        (20, 10, 'Beginner')
        """
    )

    db.session.execute(languages_query)
    db.session.commit()

    posts_query = text(
        """
        INSERT INTO community_posts (title, content, author_id, created_at) VALUES
        ('The Joys of Learning Spanish', '¡Hola! Sharing my experiences and tips for learning Spanish.', 1, NOW()),
        ('Exploring French Culture Through Language', 'Bonjour! Let''s dive into the world of French language and culture.', 2, NOW()),
        ('Tips for Efficient Language Learning', 'Sharing my strategies for effective language learning. What are yours?', 3, NOW()),
        ('The Beauty of Multilingualism', 'Discussing the advantages and joys of being multilingual. Join the conversation!', 4, NOW()),
        ('Language Exchange Opportunities', 'Looking for language exchange partners. Let''s learn together!', 5, NOW()),
        ('Mastering Mandarin: Challenges and Triumphs', 'Embarking on a journey to master Mandarin. Share your experiences!', 6, NOW()),
        ('Connecting Through Language: Cultural Exchange Stories', 'Share your stories of cultural exchange through language learning.', 7, NOW()),
        ('Language Learning Challenges: Overcoming Obstacles', 'Discussing common challenges in language learning and how to overcome them.', 8, NOW()),
        ('Exploring the World of Italian Language and Culture', 'Ciao! Join me in exploring the richness of Italian language and culture.', 9, NOW()),
        ('Adventures in Japanese Language Learning', 'Konnichiwa! Sharing experiences and recommendations for learning Japanese.', 10, NOW()),
        ('Discovering the Wonders of German Grammar', 'Guten Tag! Let''s delve into the fascinating world of German grammar together.', 11, NOW()),
        ('Spanish Literature Recommendations', 'Hola amigos! Share your favorite Spanish literature and let''s build a reading list.', 12, NOW()),
        ('The Art of Pronunciation in English', 'Exploring the nuances of English pronunciation. Any tips to share?', 13, NOW()),
        ('Embracing the Challenge of Russian Cases', 'Здравствуйте! Discussing the challenges and triumphs of mastering Russian cases.', 14, NOW()),
        ('Language Learning and Technology', 'How do you use technology in your language learning journey? Let''s exchange ideas!', 15, NOW()),
        ('Cultural Exchange Through Music', 'Share your favorite international songs and the stories behind them. Music knows no language barriers!', 16, NOW()),
        ('Navigating the Complexities of Chinese Characters', '你好! Let''s share strategies for remembering and writing Chinese characters.', 17, NOW()),
        ('Bilingual Parenting Tips', 'Are you raising bilingual children? Share your experiences and tips for a multilingual family.', 18, NOW()),
        ('Exploring the Beauty of Portuguese', 'Olá! Join the conversation about the beauty of the Portuguese language and its cultural richness.', 19, NOW()),
        ('Language Learning and Travel', 'Share your language learning experiences while traveling. Any memorable encounters?', 20, NOW())
        """
    )

    db.session.execute(posts_query)
    db.session.commit()

    comments_query = text(
        """
        INSERT INTO post_comments (post_id, author_id, timestamp, content) VALUES
        (1, 2, NOW(), 'Great post! I also love learning Spanish and can share some tips.'),
        (2, 3, NOW(), 'Bonjour! Your post about French culture is fascinating. Merci!'),
        (3, 4, NOW(), 'Excellent tips for language learning. Consistency is key!'),
        (4, 5, NOW(), 'Being multilingual is indeed a beautiful experience. I resonate with your thoughts.'),
        (5, 6, NOW(), 'I am interested in language exchange. Let us connect and learn together!'),
        (6, 7, NOW(), 'Mastering Mandarin can be challenging, but it is so rewarding! 加油!'),
        (7, 8, NOW(), 'Language exchange stories are always inspiring. Thanks for sharing!'),
        (8, 9, NOW(), 'Overcoming language learning challenges is a journey worth taking. Keep it up!'),
        (9, 10, NOW(), 'Ciao! I am passionate about Italian language and culture too. Let us explore together!'),
        (10, 11, NOW(), 'Learning Japanese is exciting. Your adventures inspire me to dive into it too.'),
        (11, 12, NOW(), 'Your language journey is motivating! Keep up the good work.'),
        (12, 13, NOW(), 'I completely agree with your insights on language and culture.'),
        (13, 14, NOW(), 'How do you manage to learn multiple languages simultaneously?'),
        (14, 15, NOW(), 'Let us share language learning resources!'),
        (15, 16, NOW(), 'Have you tried language immersion programs?'),
        (5, 6, NOW(), 'Language exchange sounds great! I am in.'),
        (6, 7, NOW(), '加油 indeed! Mandarin is challenging but so rewarding.'),
        (7, 8, NOW(), 'I have some tips for overcoming language learning obstacles. Would you like to hear?'),
        (8, 9, NOW(), 'Your dedication to fluency is admirable. Keep going!'),
        (9, 10, NOW(), 'Ciao! Let us explore Italian language and culture together.'),
        (10, 11, NOW(), 'Japanese is on my language learning bucket list. Your adventures inspire me.'),
        (1, 2, NOW(), 'Hola! I am a fellow Spanish enthusiast. Let is share language learning experiences.'),
        (2, 3, NOW(), 'Your love for French culture is contagious. I am considering learning French too.'),
        (3, 4, NOW(), 'Tips for language learning consistency? I struggle with that.'),
        (4, 5, NOW(), 'Being multilingual opens doors to diverse perspectives. Exciting journey!'),
        (5, 6, NOW(), 'Count me in for language exchange!'),
        (6, 7, NOW(), 'Learning Mandarin characters can be tricky. Any advice on that?'),
        (7, 8, NOW(), 'Your language exchange stories are inspiring. I have made friends through language too.'),
        (8, 9, NOW(), 'Overcoming language challenges is part of the fun. Keep the motivation high!'),
        (9, 10, NOW(), 'Ciao amico! Let us explore the beauty of Italian together.'),
        (10, 11, NOW(), 'Japanese characters seem complex, but I am eager to learn.'),
        (11, 12, NOW(), 'Your passion for languages resonates with me. Keep exploring!'),
        (12, 13, NOW(), 'Linguistics is a fascinating field. How do you approach language learning?'),
        (13, 14, NOW(), 'Managing diverse languages can be challenging. Any tips for staying organized?'),
        (14, 15, NOW(), 'Multilingualism is a gift. Let us celebrate the beauty of languages!'),
        (15, 16, NOW(), 'Interested in a language exchange? Let us connect!'),
        (16, 17, NOW(), 'Learning Mandarin tones requires practice. How did you master them?'),
        (17, 18, NOW(), 'Global connections through language are enriching. Thanks for sharing your journey.'),
        (18, 19, NOW(), 'Challenges in language learning are stepping stones to fluency. Keep going!'),
        (19, 20, NOW(), 'Ciao bella! Let us explore Italian culture together.'),
        (20, 20, NOW(), 'Japanese language has unique nuances. Excited to learn more!')
        """
    )
    db.session.execute(comments_query)

    db.session.commit()