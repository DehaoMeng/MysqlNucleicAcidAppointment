/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 80016
 Source Host           : localhost:3306
 Source Schema         : nucleicacidinformationbase

 Target Server Type    : MySQL
 Target Server Version : 80016
 File Encoding         : 65001

 Date: 02/07/2022 14:36:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for appointmentable
-- ----------------------------
DROP TABLE IF EXISTS `appointmentable`;
CREATE TABLE `appointmentable`  (
  `Uno` char(18) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Sno` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `AppointmentDate` date NOT NULL,
  `Timing` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '09:00-12:00',
  `VerificationCode` char(12) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'null',
  `Status` char(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '否',
  PRIMARY KEY (`Uno`, `AppointmentDate`, `Timing`) USING BTREE,
  UNIQUE INDEX `VerificationCode`(`VerificationCode`) USING BTREE,
  INDEX `Sno`(`Sno`) USING BTREE,
  CONSTRAINT `appointmentable_ibfk_1` FOREIGN KEY (`Uno`) REFERENCES `usertable` (`Uno`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `appointmentable_ibfk_2` FOREIGN KEY (`Sno`) REFERENCES `samplingpointable` (`Sno`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of appointmentable
-- ----------------------------
INSERT INTO `appointmentable` VALUES ('120223200204245552', '1902E04', '2021-10-30', '09:00-12:00', '041030000001', '是');

-- ----------------------------
-- Table structure for resultable
-- ----------------------------
DROP TABLE IF EXISTS `resultable`;
CREATE TABLE `resultable`  (
  `VerificationCode` char(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Result` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '阴性',
  PRIMARY KEY (`VerificationCode`) USING BTREE,
  CONSTRAINT `resultable_ibfk_1` FOREIGN KEY (`VerificationCode`) REFERENCES `appointmentable` (`VerificationCode`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resultable
-- ----------------------------
INSERT INTO `resultable` VALUES ('041030000001', '阴性');

-- ----------------------------
-- Table structure for samplingpointable
-- ----------------------------
DROP TABLE IF EXISTS `samplingpointable`;
CREATE TABLE `samplingpointable`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `SName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Sno` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Amount` int(11) NULL DEFAULT 0,
  PRIMARY KEY (`Sno`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of samplingpointable
-- ----------------------------
INSERT INTO `samplingpointable` VALUES (9, '京江报告厅', '1902E04', 0);
INSERT INTO `samplingpointable` VALUES (12, '大学生创业孵化基地', '1902N02', 0);
INSERT INTO `samplingpointable` VALUES (11, '学苑楼', '1902N03', 0);
INSERT INTO `samplingpointable` VALUES (10, '研究生报告厅', '1902W01', 0);

-- ----------------------------
-- Table structure for usertable
-- ----------------------------
DROP TABLE IF EXISTS `usertable`;
CREATE TABLE `usertable`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Uname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Uno` char(18) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Sex` char(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '_utf8mb4\\\'ç·\\\'',
  PRIMARY KEY (`Uno`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  UNIQUE INDEX `Uno`(`Uno`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of usertable
-- ----------------------------
INSERT INTO `usertable` VALUES (1, '孟德昊', '120223200204245552', '男');
INSERT INTO `usertable` VALUES (2, '张金娟', '522227199912260442', '女');

-- ----------------------------
-- Triggers structure for table appointmentable
-- ----------------------------
DROP TRIGGER IF EXISTS `AfterCompleteAppoint`;
delimiter ;;
CREATE TRIGGER `AfterCompleteAppoint` AFTER UPDATE ON `appointmentable` FOR EACH ROW BEGIN
 IF(new.Status!=old.Status) then
 UPDATE SamplingPoinTable set Amount = Amount-1 WHERE Sno=old.Sno;
 END IF;
 END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table appointmentable
-- ----------------------------
DROP TRIGGER IF EXISTS `Deleteappoint`;
delimiter ;;
CREATE TRIGGER `Deleteappoint` AFTER DELETE ON `appointmentable` FOR EACH ROW begin
 IF (old.Status="否") then
 Update SamplingPoinTable set Amount = Amount-1 WHERE Sno=old.Sno;
 END IF;
 END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table appointmentable
-- ----------------------------
DROP TRIGGER IF EXISTS `Appoint`;
delimiter ;;
CREATE TRIGGER `Appoint` AFTER INSERT ON `appointmentable` FOR EACH ROW BEGIN
 IF(new.VerificationCode!='null') then
 UPDATE SamplingPoinTable set Amount = Amount+1 WHERE Sno=new.Sno;
 END IF;
 END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table resultable
-- ----------------------------
DROP TRIGGER IF EXISTS `AfterResult`;
delimiter ;;
CREATE TRIGGER `AfterResult` AFTER INSERT ON `resultable` FOR EACH ROW BEGIN
 UPDATE Appointmentable set Status="是" WHERE 	Appointmentable.VerificationCode=new.VerificationCode;
 END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
