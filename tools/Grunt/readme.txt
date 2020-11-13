Do not use the standard user-agent strings in the grunt listener, replace them with alternatives.
https://developers.whatismybrowser.com/useragents/explore/


Replace line 1094 of the default ExecutorCode in the grunt template within Covenant (Private static string GruntEncryptedMessageFormat) with the line below:
@"{{""???G?U?I??D"":""{0}"",""T?y?p???e"":{1},""?M???e?t?a"":""{2}"",""?I?V?"":""{3}"",""??E?n?cry?pt?e?d?M?e???ss?a?g?e?"":""{4}"",""??H????M?A??C???"":""{5}""}}".Replace("?","");'

