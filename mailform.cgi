#!/usr/bin/perl

#******************************************************************************
#	設定項目
# 修正必要
#******************************************************************************
$jcode = 'jcode.pl';
$sendmail = '/usr/sbin/sendmail';
$srvtyp = "sendmail";
$tempfile = './tempfile.dat';
$getmail = 'kunifuda@ark-d.biz,info@c-e-m.co.jp';
$complete = 'form-ok.html';
$mailfrom = '=?ISO-2022-JP?B?GyRCM3Q8MDJxPFIlNyE8JSghPCUoJWAbKEI=?= <info@c-e-m.co.jp>';
$checktemplete = 'form-check.html';
$errortemplete = 'form-error.html';
$titleinput = '=?ISO-2022-JP?B?GyRCJCpMZCQkOWckbyQ7JCIkaiQsJEgkJiQ0JDYkJCReJDkhWjwrRjBKVj8uJWEhPCVrIVsbKEI=?=';
$subtitle = "";
$blckdelimita = '_##_';
$indidelimita = '<br>';
$maildelimita = '\n';
@denyword = ();
@denyhost = ();
$denydouble = 0;
$denyother = 0;
$fromisreceiver = 1;
$enterformurl = 'contact.html';
$ownurl = 'mailform.cgi';
$metajump = 0;
$maxupsize = 5191680;
@allowext = ();
$upload_fil = "";
$upload_tmp = "";
$upload_dir = './upload';

#******************************************************************************
#	メインルーチン
#******************************************************************************

require $jcode;

	#
	#	環境変数チェック
	#
	
	$sndtype = "normal";
	
	if ( $ENV{'CONTENT_TYPE'} =~ /^multipart*/ )
	{
		$sndtype = "multipart";
	}

	#
	# 	POSTデータ受信セクション
	#
	
	if ( $sndtype eq "multipart" )
	{
		#
		# 	マルチパートPOSTデータ受信
		#
	
		$tmpbuf = "";
		$postdt = "";
		$remain = $ENV{'CONTENT_LENGTH'};
	
		binmode(STDIN);
		while ($remain) 
		{
			$remain -= sysread(STDIN, $tmpbuf, $remain);
			$postdt .= $tmpbuf;
		}

		#
		#	POSTデータ解析
		#

		$delmtr = "";
		$dtpos1 = 0;
		$dtpos2 = 0;
		$dtpos3 = 0;
		
		while (1) 
		{
			#
			# 	ヘッダ部分処理
			#
			$dtpos2 = index($postdt, "\r\n\r\n", $dtpos1) + 4;
			@headrs = split("\r\n", substr($postdt, $dtpos1, $dtpos2 - $dtpos1));
			$filnam = "";
			$keynam = "";
			foreach (@headrs) 
			{
				if ($delmtr eq "") 
				{
					$delmtr = $_;
			    } 
			    elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"; filename="([^;]*)"/i) 
			    {
					if ($3) 
					{
						$filnam = $3;
						if ($filnam =~ /([^\\\/]+$)/) 
						{
							$filnam = $1;
						}
					}
				}
				elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"/i) 
				{
					$keynam = $2;
				}
			}

			#
			# 	本体の処理
			#

			$tmpary = "";
			$dtpos3 = index($postdt, "\r\n$delmtr", $dtpos2);
			$dtsize = $dtpos3 - $dtpos2;

			if ($filnam) 
			{
				&error("ファイルサイズが大きすぎます") if ( $maxupsize > 0 && $dtsize > $maxupsize ) ;
				$filnam =~ /(.*)(\.)(.*)/;
				$uppnam = &MakeTempFileName( $filnam );
				if (open(OUT, "> $upload_dir/$uppnam")) 
				{
					$upload_fil=$filnam;
					$upload_tmp=$uppnam;
					binmode(OUT);
					print OUT substr($postdt, $dtpos2, $dtsize);
					close(OUT);
				}
			} 
			elsif ($keynam) 
			{
				$FRMINPUT{$keynam} = substr($postdt, $dtpos2, $dtsize);
			}

			#
			#	次レコード検出処理
			#

			$dtpos1 = $dtpos3 + length("\r\n$delmtr");
			if (substr($postdt, $dtpos1, 4) eq "--\r\n") 
			{
				last;
			} 
			else 
			{
				$dtpos1 += 2;
				if ($max_count++ > 99999) 
				{ 
					last; 
				}
				next;
			}
		}
	}
	else
	{
		#
		# 	ノーマルPOSTデータ受信
		#

		$cl = $ENV{"CONTENT_LENGTH"};

		if( $cl > 0 )
		{
			read(STDIN, $qs, $cl );
		} else {
			$qs = $ENV{"QUERY_STRING"};
		}	
	
		@contents = split(/&/,$qs);
		foreach $i (0 .. $#contents) 
		{
			local($key,$text)= split(/=/,$contents[$i]);
			$FRMINPUT{$key} = $text;
		}
	}
	
	#
	#	本処理スタート
	#
	
	foreach my $key ( sort keys %FRMINPUT )
	{
		$text = $FRMINPUT{$key};
		$text =~ s/\+/ /g;
		$text =~ s/%(..)/pack("c",hex($1))/ge;
		$text =~ s/\r\n/\n/g; 
		$text =~ s/\r/\n/g; 
		&jcode'convert(*text,"euc"); 
		$act = $text if $key eq 'act';
		$sndtype = $text if $key eq 'sndtype';
		$delmtr = $text if $key eq 'delmtr';

		$datatitle[$1] = $text if $key =~ /^datatitle(\d+)/i;
		$datacheck[$1] = $text if $key =~ /^datacheck(\d+)/i;
		$datatypes[$1] = $text if $key =~ /^datatypes(\d+)/i;
		if ($key =~ /^data(\d+)/i)
		{
			$data[$1] .= "$blckdelimita" if $data[$1] ne "";
			$data[$1] .= $text;
			$data[$1] =~ s/</&lt;/g;
			$data[$1] =~ s/>/&gt;/g;
			#$data[$1] =~ s/\n/<br>\n/g; 
		}
		if ($key =~ /^subdata(\d+)/i)
		{
			$subdata[$1] .= "$blckdelimita" if $subdata[$1] ne "";
			$subdata[$1] .= $text;
			$subdata[$1] =~ s/</&lt;/g;
			$subdata[$1] =~ s/>/&gt;/g;
			#$subdata[$1] =~ s/\n/<br>\n/g; 
		}
	}

	for(1 .. 99)
	{
		last if $datatitle[$_] eq "";
		if ( $datatypes[$_] eq "itm10" && $data[$_] eq "" && $upload_fil ne "")
		{
			$data[$_] = $upload_fil;
			$subdata[$_] = $upload_tmp;
		}
		elsif ( $datatypes[$_] eq "itm09" && $data[$_] ne "" )
		{
			$data[$_] =~ s/$blckdelimita/,/g;
		}
	}

	$ip			= $ENV{'REMOTE_ADDR'};
	$host		= gethostbyaddr(pack("C4", split(/\./, $ip)), 2);
	$host		= $ENV{'REMOTE_HOST'} if $host eq "";
	$host		= $ip if $host eq "";
	$useragent	= $ENV{'HTTP_USER_AGENT'};
	$referer	= $ENV{'HTTP_REFERER'};

	if (($act eq "") || (($denyother) && (($ENV{'HTTP_REFERER'} !~ /$enterformurl/i) && ($ENV{'HTTP_REFERER'} !~ /$ownurl/))))
	{
		&jump($enterformurl);
	}
	elsif ($act eq "check")	
	{
		&check;
	}
	elsif ($act eq "send")	
	{
		&send;
	}

	exit;

#*****************************************************************************
#	入力データチェック
#*****************************************************************************
sub datacheck
{
	while(1)
	{
		last if ( !(chomp($message)) )
	}

	if ($denyhost[0])
	{
		foreach(@denyhost)
		{
			&error("あなたの接続元からは送信できません。") if (index($host,$_) != -1) || (index($ip,$_) != -1);
		}
	}
	for(1 .. 99)
	{
		last if $datatitle[$_] eq "";
		&error("$datatitle[$_]のデータを入力してください。") if ($datacheck[$_]) && ($data[$_] eq "");

		if ( ($datatypes[$_] eq "itm04") || ($datatypes[$_] eq "itm03") )
		{
			&error("$datatitle[$_]のメールアドレスが間違っています。") if ($data[$_] !~ /[\w\.\-\&]+\@[\w\.\-\&]+\.[\w\.\-\&]/);
			if ( $datatypes[$_] eq "itm04" )
			{
				&error("$datatitle[$_]の再入力項目のメールアドレスが間違っています。") if ($subdata[$_] !~ /[\w\.\-\&]+\@[\w\.\-\&]+\.[\w\.\-\&]/);
				&error("$datatitle[$_]の再入力項目のメールアドレスを入力してください。") if ($subdata[$_] eq "");
				&error("$datatitle[$_]が間違っています。") if ( $data[$_] ne $subdata[$_] );
			}
		}
		elsif ( $datatypes[$_] eq "itm10" && $allowext[0])
		{
			$ext = $data[$_];
			if($ext =~ m/\.([^\.][0-9a-zA-Z]*)$/)
			{
				$ext = $1;
			}
			$swFlag = "NG";
			foreach( @allowext )
			{
				if ( index($ext,$_) != -1 )
				{
					$swFlag = "OK";
					last;
				}
			}
			if ( $swFlag eq "NG" )
			{
				&error( "この拡張子のファイルは送信できません" ) ;
			}
		}

		if ($denyword[0])
		{
			if ( ($datatypes[$_] eq "itm01") || ($datatypes[$_] eq "itm02") || ($datatypes[$_] eq "itm07") )
			{
				$chk = $data[$_];
				foreach(@denyword)
				{
					&error("このメッセージは送信できません。") if index($chk,$_) != -1;
				}
			}
		}
	}
}

#*****************************************************************************
#	アップロード用一時ファイル名作成
#*****************************************************************************
sub MakeTempFileName
{
	my $loclFilNam ;
	my $loclTmpNam ;
	my $loclExtNam ;

	$loclFilNam = $_[0] ;
	$loclExtNam = $loclFilNam;
	
	if($loclExtNam =~ m/\.([^\.][0-9a-zA-Z]*)$/)
	{
		$loclExtNam = $1;
	}

	for ( 0..1000 )
	{
		$loclFilNam = "UPLOADTEMP$_.$loclExtNam";
		$loclTmpNam = "$upload_dir/$loclFilNam";
		
		if ( -f $loclTmpNam )
		{
		}
		else
		{
			last ;
		}
	}
	
	return $loclFilNam;
}

#*****************************************************************************
#	重複送信防止機構
#*****************************************************************************
sub CheckDupplicate
{
	if ($denydouble)
	{
		open (IO,"+<$tempfile");
		eval{flock(IO,2)};
		$temp=<IO>;
		if ($temp eq $ip)
		{
			close(IO);
			&error("連続投稿は禁止されています。");
		} else {
			close(IO);
			open (IO, "> $tempfile");
			$| = 1; # autoflush on
			print IO $ip;
			close(IO);
		}
	}
}

#*****************************************************************************
#	入力項目取得処理
#*****************************************************************************
sub GetCustomData
{
	$maildata="";
	$mailto="";
	$custnm="";

	for (1 .. 99)
	{
		last if $datatitle[$_] eq "";
		$data[$_] =~ s/$blckdelimita$//i;
		$data[$_] =~ s/$blckdelimita/$maildelimita/ig;
		$maildata.="【$datatitle[$_]】: $data[$_]\n" if $data[$_] ne "";

		if ($datatypes[$_] eq "itm02")
		{
			$custnm=$data[$_];
		}

		if (($datatypes[$_] eq "itm03") || ($datatypes[$_] eq "itm04") )
		{
			if ( $mailto ne "" )
			{
				$mailto.=","
			}
			$mailto.=$data[$_];
		}
	}
}

#*****************************************************************************
#	メール本文作成処理
#*****************************************************************************
sub GetMailContext
{
$mailbody .= "$custnm　様\n";
$mailbody .= "\n";
$mailbody .= "株式会社シーイーエムです。\n";
$mailbody .= "\n";
$mailbody .= "この度は、弊社サイトよりお問い合わせを頂き、誠にありがとうございます。\n";
$mailbody .= "\n";
$mailbody .= "まずは、フォームにてご入力頂きました内容をご確認下さいませ。\n";
$mailbody .= "\n";
$mailbody .= "-------------------------------------------------------\n";
$mailbody .= "ご入力内容\n";
$mailbody .= "-------------------------------------------------------\n";
$mailbody .= "\n";
$mailbody .= "$maildata\n";
$mailbody .= "\n";
$mailbody .= "お問い合わせの内容を確認の上、弊社スタッフより返信させて頂きますので\n";
$mailbody .= "今しばらくお待ちくださいませ。\n";
$mailbody .= "\n";
$mailbody .= "\n";
$mailbody .= "-------------------------------------------------------\n";
$mailbody .= "株式会社シーイーエム\n";
$mailbody .= "〒101-0025  東京都千代田区神田佐久間町3-37　山本ﾋﾞﾙ3F\n";
$mailbody .= "TEL : 03-3863-7403   FAX : 03-3863-7008\n";
$mailbody .= "E-mail : info\@c-e-m.co.jp\n";
$mailbody .= "http://www.c-e-m.co.jp\n";
$mailbody .= "-------------------------------------------------------\n";
$mailbody .= "\n";
}

#*****************************************************************************
#	メールサブコンテキスト作成処理
#*****************************************************************************
sub GetMailSubText
{
$mailbody2  = "";
$mailbody2 .= <<EOD;
-----------------------------------------------------------
投稿者の情報
IPアドレス：$ip
ホスト名：$host
ユーザーエージェント：$useragent
リファラー：$referer
-----------------------------------------------------------
EOD
}

#*****************************************************************************
#	メール送信
#*****************************************************************************
sub SendMailData
{
	$tmpMail = $_[0];
	$namMail = $_[1];
	
	&jcode::convert(\$tmpMail,'jis');
	
	if ( $srvtyp eq "winSMTPservice" )
	{
		open(MAIL,"> $sendmail\\$namMail -t") || die &error("SMTP Serviceが使用できませんでした。");
	}
	else
	{
		open(MAIL,"| $sendmail -t") || die &error("sendmailが使用できませんでした。");
	}
	print MAIL $tmpMail;
	close (MAIL);
	sleep(1);
}

#*****************************************************************************
#	BASE64変換
#*****************************************************************************
sub base64encode 
{
	my $str = shift;
	my $table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
	my $ret;
	my $cnt;
	my ($i, $j, $x, $y);
    $cnt=0;
	for($i=$x=0, $j=2; $i<length($str); $i++) 
	{
		$x    = ($x<<8) + ord(substr($str,$i,1));
		$ret .= substr($table, ($x>>$j) & 0x3f, 1);

		if ( $cnt++ > 76 ) { $cnt=0; $ret.="\n";}

		if ($j != 6) { $j+=2; next; }

		$ret .= substr($table, $x & 0x3f, 1);
		$j    = 2;
		
		if ( $cnt++ > 76 ) { $cnt=0; $ret.="\n";}
	}
	if ($j != 2)    { $ret .= substr($table, ($x<<(8-$j)) & 0x3f, 1); }
	if ($j == 4)    { $ret .= '=='; }
	elsif ($j == 6) { $ret .= '=';  }

	return $ret;
}

#*****************************************************************************
#	拡張子をMIMEに変換
#*****************************************************************************
sub ConvertExtToMime
{
	%mimecnv = ();
	$mimecnv{'pdf'} = "application/pdf";
	$mimecnv{'jpg'} = "image/jpg";
	$mimecnv{'bmp'} = "image/bmp";
	$mimecnv{'gip'} = "image/gif";
	$mimecnv{'png'} = "image/png";
	$mimecnv{'zip'} = "application/x-zip-compressed";

	$exp = $_[0] ;

	while ( ( $key , $text ) = each %mimecnv )
	{
		if ( $key eq $exp )
		{
			return $text ;
		}
	}

	return "application/octet-stream";
}
#*****************************************************************************
#	通常メール作成処理
#*****************************************************************************
sub SendNormlMail
{
	$mailhead .= "Subject: $titleinput$subtitle\n";
	$mailhead .="Content-Transfer-Encoding: 7bit\n";
	$mailhead .="Content-Type: text/plain; charset=ISO-2022-JP\n";
	$mailhead .="X-Mailer: melsaku\n";

	&GetCustomData;
	&GetMailContext;
	&GetMailSubText;

	#
	#  本人宛メールの送信
	#

	if ( $mailto ne "" )
	{
		$temp = "To: $mailto\nFrom: $mailfrom\n";
		$temp .= $mailhead.$mailbody."\n";
		&SendMailData($temp,"mail01.txt");
	}

	#
	#  コピーメールの送信
	#

	if ( $fromisreceiver && $mailto ne "" )
	{
		$mailfrom = $mailto ;
	}

	$gree = "\n【　コピーメールです 】\n\n";
	$temp = "To: $getmail\nFrom: $mailfrom\n";
	$temp .= $mailhead.$gree.$mailbody.$mailbody2."\n";
	&SendMailData($temp,"mail02.txt");
}

#*****************************************************************************
#	添付ファイル付きメール作成処理
#*****************************************************************************
sub SendMultiMail
{
	#
	#	添付ファイル名を取得する
	#
	
	$tempName = "";
	
	for(1 .. 99)
	{
		last if $datatitle[$_] eq "";

		if ( $datatypes[$_] eq "itm10" && $data[$_] ne "" )
		{
			$tempServ = $subdata[$_];
			$tempName = $data[$_];
			$tempChek = $datacheck[$_];
			last;
		}
	}

	if ( $tempName eq "" )
	{
		&error( "添付ファイルが指定されていませんでした" ) if ( $tempChek );
	}

	#
	#	拡張子を取得する
	#
	
	$ext = $tempName ;
	
	if($ext =~ m/\.([^\.][0-9a-zA-Z]*)$/)
	{
		$ext = $1;
	}
	
	$extMime = ConvertExtToMime( $ext );
	
	#
	#	メール作成開始
	#
	
	&GetCustomData;
	&GetMailContext;
	&GetMailSubText;

	#
	#	添付ファイル
	#
	
	$mimeBuff = "";
	open(IN,"$upload_dir/$tempServ");
	while(<IN>)
	{
		$mimeBuff.=$_;
	}
	close(IN);

	$mimeMail = &base64encode($mimeBuff);
	
	#
	#	メール組立
	#

	$mimeTopHead  = "";
	$mimeTopHead .= "Subject: $titleinput$subtitle\n";
	$mimeTopHead .= "MIME-Version: 1.0\n";
	$mimeTopHead .= "Content-Type: multipart/mixed;\n\tboundary=\"$delmtr\"\n";
	$mimeTopHead .= "Content-Transfer-Encoding: 7bit\n";
	$mimeTopHead .= "X-Mailer: melsaku\n\n";

	$mimeTxtHead  = "";
	$mimeTxtHead .= "--$delmtr\n";
	$mimeTxtHead .= "Content-Type: text/plain; charset=ISO-2022-JP\n\n";

	$jisNamMimes = $tempName;
	&jcode::convert(\$jisNamMimes,'jis');

	$filNamMimes  = "=?ISO-2022-JP?B?";
	$filNamMimes .= &base64encode($jisNamMimes);
	$filNamMimes .= "?=";

	$mimeFilHead  = "";
	$mimeFilHead .= "--$delmtr\n";
	$mimeFilHead .= "Content-Type: $extMime; name=\"$filNamMimes\"\n";
	$mimeFilHead .= "Content-Disposition: attachment; filename=\"$filNamMimes\"\n";
	$mimeFilHead .= "Content-Transfer-Encoding: base64\n\n";
	
	$mimeEndHead  = "";
	$mimeEndHead .= "\n--$delmtr--\n\n";

	#
	#	本人宛メールの送信
	#

	if ( $mailto ne "" )
	{
		$temp = "To: $mailto\nFrom: $mailfrom\n";
		$temp .= $mimeTopHead;
		$temp .= $mimeTxtHead;
		$temp .= $mailbody."\n";
		if ( $tempName ne "" )
		{
			$temp .= $mimeFilHead;
			$temp .= $mimeMail;
		}
		$temp .= $mimeEndHead;
		&SendMailData($temp,"mail01.txt");
	}
	
	#
	#	コピーメールの送信
	#

	if ( $fromisreceiver && $mailto ne "" )
	{
		$mailfrom = $mailto ;
	}

	$gree  = "\n【　コピーメールです 】\n\n";
	$temp  = "To: $getmail\nFrom: $mailfrom\n";
	$temp .= $mimeTopHead;
	$temp .= $mimeTxtHead;
	$temp .= $gree;
	$temp .= $mailbody.$mailbody2."\n";
	if ( $tempName ne "" )
	{
		$temp .= $mimeFilHead;
		$temp .= $mimeMail;
	}
	$temp .= $mimeEndHead;

	&SendMailData($temp,"mail02.txt");

	#
	#	添付ファイルの削除
	#

	unlink( "$upload_dir/$tempServ" );

}

#*****************************************************************************
#	メール送信
#*****************************************************************************
sub send
{
	&datacheck;
	my ($temp);

	&CheckDupplicate;

	if ( $sndtype eq "multipart" )
	{
		&SendMultiMail;
	}
	else
	{
		&SendNormlMail;
	}

	&jump($complete);
}

#*****************************************************************************
#	入力確認
#*****************************************************************************
sub check
{
	#入力確認画面
	&datacheck;

	my ($buffer,$buffer2,$temp);
	open(IN,"$checktemplete");
	while(<IN>)
	{
		$buffer2.=$_;
	}
	close(IN);

	$temp = $message;
	$temp =~ s/\n/$indidelimita/ig;
	$buffer2 =~ s/<!--TITLE-->/$titleinput/ig;

$buffer = <<EOD;
<input type="hidden" name="title" value="$titleinput">
<input type="hidden" name="sndtype" value="$sndtype">
<input type="hidden" name="delmtr" value="$delmtr">
EOD

	for(1 .. 99)
	{
		last if $datatitle[$_] eq "";
		$data[$_] =~ s/$blckdelimita$//ig;
		$buffer.=<<EOD;
<input type="hidden" name="datatitle$_" value="$datatitle[$_]">
<input type="hidden" name="datacheck$_" value="$datacheck[$_]">
<input type="hidden" name="datatypes$_" value="$datatypes[$_]">
<input type="hidden" name="data$_" value="$data[$_]">
<input type="hidden" name="subdata$_" value="$subdata[$_]">
EOD
		$temp = $data[$_];
		$temp =~ s/$blckdelimita/$indidelimita/ig;
		$temp =~ s/\n/<BR>/ig;
		$buffer2 =~ s/<!--DATA$_-->/$temp/ig;
	}
	$buffer2 =~ s/<!--ALLDATA-->/$buffer/ig;

	print "Content-type:text/html; charset= EUC-JP\n\n".$buffer2;
	exit;
}

#*****************************************************************************
#	エラー表示
#*****************************************************************************
sub error
{
	print "Content-type:text/html; charset=EUC-JP\n\n";
	open (IN,"$errortemplete");
	while(<IN>)
	{
		$_ =~ s/<!--ERROR-->/$_[0]/ig;
		print;
	}
	close(IN);
	exit;
}

#*****************************************************************************
#	ページジャンプ
#*****************************************************************************
sub jump
{
	if ($metajump == 0)
	{
		print "Location: $_[0]\n\n";
	} else {
print <<EOD;
Content-type:text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="refresh" content="0;url=$_[0]">
<title>Waiting...</title>
</head>
<body>
</body>
</html>
EOD
	}
	exit;
}
