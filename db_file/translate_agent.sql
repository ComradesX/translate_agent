/*
 Navicat Premium Dump SQL

 Source Server         : mysql57
 Source Server Type    : MySQL
 Source Server Version : 50743 (5.7.43)
 Source Host           : localhost:3307
 Source Schema         : translate_agent

 Target Server Type    : MySQL
 Target Server Version : 50743 (5.7.43)
 File Encoding         : 65001

 Date: 18/05/2026 09:49:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL COMMENT '文件名',
  `file_path` varchar(500) NOT NULL COMMENT '文件地址',
  `content` longtext NOT NULL COMMENT '文章完整内容',
  `language_type` varchar(20) NOT NULL COMMENT '语言类型，如 en、zh',
  `upload_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of article
-- ----------------------------
BEGIN;
INSERT INTO `article` (`id`, `filename`, `file_path`, `content`, `language_type`, `upload_time`) VALUES (1, 'IHaveADream.txt', '/Users/xiaoshicheng/python_projects/translate_agent/src/resource/uploads/IHaveADream_aa7633a3f7fd47ceacdb417edea08a63.txt', 'Five score years ago (note: 100 years ago), a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice. It came as a joyous daybreak to end the long night of bad captivity.\nBut one hundred years later, the Negro still is not free. One hundred years later, the life of the Negro is still sadly crippled by the manacles of segregation and the chains of discrimination. One hundred years later, the Negro lives on a lonely island of poverty in the midst of a vast ocean of material prosperity. One hundred years later, the Negro is still languished in the corners of American society and finds himself an exile in his own land. And so we\'ve come here today to dramatize a shameful condition.\nWe have also come to this hallowed spot to remind America of the fierce urgency of now. This is no time to engage in the luxury of cooling off or to take the tranquilizing drug of gradualism. Now is the time to make real the promises of democracy. Now is the time to rise from the dark and desolate valley of segregation to the sunlit path of racial justice. Now is the time to lift our nation from the quick sands of racial injustice to the solid rock of brotherhood. Now is the time to make justice a reality for all of God\'s children.\n\nIn a sense we\'ve come to our nation\'s capital to cash a check. When the architects of our republic wrote the magnificent words of the Constitution and the Declaration of Independence, they were signing a promissory note to which every American was to fall heir. This note was a promise that all men, yes, black men as well as white men, would be guaranteed the \"unalienable Rights\" of \"Life, Liberty and the pursuit of Happiness.\"\nIt is obvious today that America has defaulted on this promissory note, insofar as her citizens of color are concerned. Instead of honoring this sacred obligation, America has given the Negro people a bad check, a check which has come back marked \"insufficient funds.\" But we refuse to believe that the bank of justice is bankrupt. We refuse to believe that there are insufficient funds in the great vaults of opportunity of this nation. And so we\'ve come to cash this check, a check that will give us upon demand the riches of freedom and the security of justice.\nLet us not seek to satisfy our thirst for freedom by drinking from the cup of bitterness and hatred. We must forever conduct our struggle on the high plane of dignity and discipline. We must not allow our creative protest to degenerate into physical violence. Again and again we must rise to the majestic heights of meeting physical force with soul force.\nThe marvelous new militancy which has engulfed the Negro community must not lead us to distrust of all white people, for many of our white brothers, as evidenced by their presence here today, have come to realize that their destiny is tied up with our destiny and their freedom is inextricably bound to our freedom. We cannot walk alone. And as we walk, we must make the pledge that we shall march ahead. We cannot turn back.\nThere are those who are asking the devotees of civil rights, \"When will you be satisfied?\" We can never be satisfied as long as our bodies, heavy with the fatigue of travel, cannot gain lodging in the motels of the highways and the hotels of the cities. We cannot be satisfied as long as the Negro\'s basic mobility is from a smaller ghetto to a larger one. We can never be satisfied as long as a Negro in Mississippi cannot vote and a Negro in New York believes he has nothing for which to vote. No, no, we are not satisfied, and we will not be satisfied until justice rolls down like waters and righteousness like a mighty stream.\nI am not unmindful that some of you have come here out of great trials and tribulations. Some of you have come fresh from narrow cells. Some of you have come from areas where your quest for freedom left you battered by the storms of persecution and staggered by the winds of police brutality. You have been the veterans of creative suffering. Continue to work with the faith that unearned suffering is redemptive. Go back to Mississippi, go back to Alabama, go back to Georgia, go back to Louisiana, go back to the slums and ghettos of our northern cities, knowing that somehow this situation can and will be changed. Let us not wallow in the valley of despair.\n\nI say to you today, my friends, that in spite of the difficulties and frustrations of the moment, I still have a dream. It is a dream deeply rooted in the American dream.\nI have a dream that one day this nation will rise up and live out the true meaning of its creed: \"We hold these truths to be self-evident: that all men are created equal.\"\nI have a dream that one day on the red hills of Georgia the sons of former slaves and the sons of former slaveowners will be able to sit down together at a table of brotherhood.\nI have a dream that one day even the state of Mississippi, a desert state, sweltering with the heat of injustice and oppression, will be transformed into an oasis of freedom and justice.\nI have a dream that my four children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.\nI have a dream that one day the state of Alabama, whose governor\'s lips are presently dripping with the words of interposition and nullification, will be transformed into a situation where little black boys and black girls will be able to join hands with little white boys and white girls and walk together as sisters and brothers.\nI have a dream that one day every valley shall be exalted, every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight, and the glory of the Lord shall be revealed, and all flesh shall see it together.\n\nThis is our hope. This is the faith with which I return to the South. With this faith we will be able to hew out of the mountain of despair a stone of hope. With this faith we will be able to transform the jangling discords of our nation into a beautiful symphony of brotherhood. With this faith we will be able to work together, to pray together, to struggle together, to go to jail together, to stand up for freedom together, knowing that we will be free one day.\nThis will be the day when all of God\'s children will be able to sing with a new meaning, \"My country, \'tis of thee, sweet land of liberty, of thee I sing. Land where my fathers died, land of the pilgrim\'s pride, from every mountainside, let freedom ring.\"\nAnd if America is to be a great nation this must become true. So let freedom ring from the prodigious hilltops of New Hampshire. Let freedom ring from the mighty mountains of New York. Let freedom ring from the heightening Alleghenies of Pennsylvania! Let freedom ring from the snowcapped Rockies of Colorado! Let freedom ring from the curvaceous peaks of California!\nBut not only that; let freedom ring from Stone Mountain of Georgia! Let freedom ring from Lookout Mountain of Tennessee! Let freedom ring from every hill and molehill of Mississippi - from every mountainside. Let freedom ring.\nAnd when this happens, and when we allow freedom to ring, when we let it ring from every village and every hamlet, from every state and every city, we will be able to speed up that day when all of God\'s children—black men and white men, Jews and Gentiles, Protestants and Catholics—will be able to join hands and sing in the words of the old Negro spiritual:\n\"Free at last! Free at last! Thank God Almighty, we are free at last!\"', 'english', '2026-05-18 09:47:15');
COMMIT;

-- ----------------------------
-- Table structure for article_sentence
-- ----------------------------
DROP TABLE IF EXISTS `article_sentence`;
CREATE TABLE `article_sentence` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `article_id` bigint(20) NOT NULL COMMENT '所属文章ID',
  `sentence_content` text NOT NULL COMMENT '句子内容',
  `sentence_index` int(11) NOT NULL COMMENT '第几句，从1开始',
  `language_type` varchar(20) NOT NULL COMMENT '语言类型',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_article_sentence_index` (`article_id`,`sentence_index`),
  KEY `idx_article_id` (`article_id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of article_sentence
-- ----------------------------
BEGIN;
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (1, 1, 'Five score years ago (note: 100 years ago), a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation.', 1, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (2, 1, 'This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice.', 2, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (3, 1, 'It came as a joyous daybreak to end the long night of bad captivity.', 3, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (4, 1, 'But one hundred years later, the Negro still is not free.', 4, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (5, 1, 'One hundred years later, the life of the Negro is still sadly crippled by the manacles of segregation and the chains of discrimination.', 5, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (6, 1, 'One hundred years later, the Negro lives on a lonely island of poverty in the midst of a vast ocean of material prosperity.', 6, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (7, 1, 'One hundred years later, the Negro is still languished in the corners of American society and finds himself an exile in his own land.', 7, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (8, 1, 'And so we\'ve come here today to dramatize a shameful condition.', 8, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (9, 1, 'We have also come to this hallowed spot to remind America of the fierce urgency of now.', 9, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (10, 1, 'This is no time to engage in the luxury of cooling off or to take the tranquilizing drug of gradualism.', 10, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (11, 1, 'Now is the time to make real the promises of democracy.', 11, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (12, 1, 'Now is the time to rise from the dark and desolate valley of segregation to the sunlit path of racial justice.', 12, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (13, 1, 'Now is the time to lift our nation from the quick sands of racial injustice to the solid rock of brotherhood.', 13, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (14, 1, 'Now is the time to make justice a reality for all of God\'s children.', 14, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (15, 1, 'In a sense we\'ve come to our nation\'s capital to cash a check.', 15, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (16, 1, 'When the architects of our republic wrote the magnificent words of the Constitution and the Declaration of Independence, they were signing a promissory note to which every American was to fall heir.', 16, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (17, 1, 'This note was a promise that all men, yes, black men as well as white men, would be guaranteed the \"unalienable Rights\" of \"Life, Liberty and the pursuit of Happiness.\"', 17, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (18, 1, 'It is obvious today that America has defaulted on this promissory note, insofar as her citizens of color are concerned.', 18, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (19, 1, 'Instead of honoring this sacred obligation, America has given the Negro people a bad check, a check which has come back marked \"insufficient funds.\"', 19, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (20, 1, 'But we refuse to believe that the bank of justice is bankrupt.', 20, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (21, 1, 'We refuse to believe that there are insufficient funds in the great vaults of opportunity of this nation.', 21, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (22, 1, 'And so we\'ve come to cash this check, a check that will give us upon demand the riches of freedom and the security of justice.', 22, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (23, 1, 'Let us not seek to satisfy our thirst for freedom by drinking from the cup of bitterness and hatred.', 23, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (24, 1, 'We must forever conduct our struggle on the high plane of dignity and discipline.', 24, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (25, 1, 'We must not allow our creative protest to degenerate into physical violence.', 25, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (26, 1, 'Again and again we must rise to the majestic heights of meeting physical force with soul force.', 26, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (27, 1, 'The marvelous new militancy which has engulfed the Negro community must not lead us to distrust of all white people, for many of our white brothers, as evidenced by their presence here today, have come to realize that their destiny is tied up with our destiny and their freedom is inextricably bound to our freedom.', 27, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (28, 1, 'We cannot walk alone.', 28, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (29, 1, 'And as we walk, we must make the pledge that we shall march ahead.', 29, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (30, 1, 'We cannot turn back.', 30, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (31, 1, 'There are those who are asking the devotees of civil rights, \"When will you be satisfied?\"', 31, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (32, 1, 'We can never be satisfied as long as our bodies, heavy with the fatigue of travel, cannot gain lodging in the motels of the highways and the hotels of the cities.', 32, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (33, 1, 'We cannot be satisfied as long as the Negro\'s basic mobility is from a smaller ghetto to a larger one.', 33, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (34, 1, 'We can never be satisfied as long as a Negro in Mississippi cannot vote and a Negro in New York believes he has nothing for which to vote.', 34, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (35, 1, 'No, no, we are not satisfied, and we will not be satisfied until justice rolls down like waters and righteousness like a mighty stream.', 35, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (36, 1, 'I am not unmindful that some of you have come here out of great trials and tribulations.', 36, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (37, 1, 'Some of you have come fresh from narrow cells.', 37, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (38, 1, 'Some of you have come from areas where your quest for freedom left you battered by the storms of persecution and staggered by the winds of police brutality.', 38, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (39, 1, 'You have been the veterans of creative suffering.', 39, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (40, 1, 'Continue to work with the faith that unearned suffering is redemptive.', 40, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (41, 1, 'Go back to Mississippi, go back to Alabama, go back to Georgia, go back to Louisiana, go back to the slums and ghettos of our northern cities, knowing that somehow this situation can and will be changed.', 41, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (42, 1, 'Let us not wallow in the valley of despair.', 42, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (43, 1, 'I say to you today, my friends, that in spite of the difficulties and frustrations of the moment, I still have a dream.', 43, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (44, 1, 'It is a dream deeply rooted in the American dream.', 44, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (45, 1, 'I have a dream that one day this nation will rise up and live out the true meaning of its creed: \"We hold these truths to be self-evident: that all men are created equal.\"', 45, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (46, 1, 'I have a dream that one day on the red hills of Georgia the sons of former slaves and the sons of former slaveowners will be able to sit down together at a table of brotherhood.', 46, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (47, 1, 'I have a dream that one day even the state of Mississippi, a desert state, sweltering with the heat of injustice and oppression, will be transformed into an oasis of freedom and justice.', 47, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (48, 1, 'I have a dream that my four children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.', 48, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (49, 1, 'I have a dream that one day the state of Alabama, whose governor\'s lips are presently dripping with the words of interposition and nullification, will be transformed into a situation where little black boys and black girls will be able to join hands with little white boys and white girls and walk together as sisters and brothers.', 49, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (50, 1, 'I have a dream that one day every valley shall be exalted, every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight, and the glory of the Lord shall be revealed, and all flesh shall see it together.', 50, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (51, 1, 'This is our hope.', 51, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (52, 1, 'This is the faith with which I return to the South.', 52, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (53, 1, 'With this faith we will be able to hew out of the mountain of despair a stone of hope.', 53, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (54, 1, 'With this faith we will be able to transform the jangling discords of our nation into a beautiful symphony of brotherhood.', 54, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (55, 1, 'With this faith we will be able to work together, to pray together, to struggle together, to go to jail together, to stand up for freedom together, knowing that we will be free one day.', 55, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (56, 1, 'This will be the day when all of God\'s children will be able to sing with a new meaning, \"My country, \'tis of thee, sweet land of liberty, of thee I sing. Land where my fathers died, land of the pilgrim\'s pride, from every mountainside, let freedom ring.\"', 56, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (57, 1, 'And if America is to be a great nation this must become true.', 57, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (58, 1, 'So let freedom ring from the prodigious hilltops of New Hampshire.', 58, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (59, 1, 'Let freedom ring from the mighty mountains of New York.', 59, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (60, 1, 'Let freedom ring from the heightening Alleghenies of Pennsylvania!', 60, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (61, 1, 'Let freedom ring from the snowcapped Rockies of Colorado!', 61, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (62, 1, 'Let freedom ring from the curvaceous peaks of California!', 62, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (63, 1, 'But not only that; let freedom ring from Stone Mountain of Georgia!', 63, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (64, 1, 'Let freedom ring from Lookout Mountain of Tennessee!', 64, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (65, 1, 'Let freedom ring from every hill and molehill of Mississippi - from every mountainside.', 65, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (66, 1, 'Let freedom ring.', 66, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (67, 1, 'And when this happens, and when we allow freedom to ring, when we let it ring from every village and every hamlet, from every state and every city, we will be able to speed up that day when all of God\'s children—black men and white men, Jews and Gentiles, Protestants and Catholics—will be able to join hands and sing in the words of the old Negro spiritual:', 67, 'english', '2026-05-18 09:47:15');
INSERT INTO `article_sentence` (`id`, `article_id`, `sentence_content`, `sentence_index`, `language_type`, `created_time`) VALUES (68, 1, '\"Free at last! Free at last! Thank God Almighty, we are free at last!\"', 68, 'english', '2026-05-18 09:47:15');
COMMIT;

-- ----------------------------
-- Table structure for llm_sentence_translation
-- ----------------------------
DROP TABLE IF EXISTS `llm_sentence_translation`;
CREATE TABLE `llm_sentence_translation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sentence_id` bigint(20) NOT NULL COMMENT '原文句子ID',
  `source_language` varchar(20) NOT NULL COMMENT '原文语言',
  `target_language` varchar(20) NOT NULL COMMENT '翻译目标语言',
  `translation_content` text NOT NULL COMMENT 'LLM翻译内容',
  `model_name` varchar(100) DEFAULT NULL COMMENT '使用的模型',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_sentence_target_model` (`sentence_id`,`target_language`,`model_name`),
  KEY `idx_sentence_id` (`sentence_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of llm_sentence_translation
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_sentence_translation
-- ----------------------------
DROP TABLE IF EXISTS `user_sentence_translation`;
CREATE TABLE `user_sentence_translation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL COMMENT '用户ID，如果暂时没有用户系统可为空',
  `article_id` bigint(20) NOT NULL COMMENT '文章ID',
  `sentence_id` bigint(20) NOT NULL COMMENT '原文句子ID',
  `target_language` varchar(20) NOT NULL COMMENT '用户翻译目标语言',
  `translation_content` text NOT NULL COMMENT '用户翻译内容',
  `ai_score` decimal(5,2) DEFAULT NULL COMMENT 'AI评分，如 0-100',
  `ai_comment` text COMMENT 'AI评语',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_article` (`user_id`,`article_id`),
  KEY `idx_sentence_id` (`sentence_id`),
  KEY `fk_user_translation_article` (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of user_sentence_translation
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
