#include "pptable.h"
#include <wx/tokenzr.h>
#include <set>

bool IsWordChar(const wxString &s, int strSize)
{
	if(strSize) {
		return s.find_first_of(wxT("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_")) != wxString::npos;

	} else {
		return s.find_first_of(wxT("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")) != wxString::npos;
	}
}

bool IsWordCharA(char c, int strSize)
{
	if(strSize) {
		return ((c >= 97 && c <= 122) ||// a-z
				(c >= 65 && c <= 90)  ||// A-Z
				(c >= 48 && c <= 57)  ||// 0-9
				(c == '_'));

	} else {
		return ((c >= 97 && c <= 122) ||// a-z
				(c >= 65 && c <= 90)  ||// A-Z
				(c == '_'));
	}
}

std::string ReplaceWordA(const std::string &str, const std::string &word, const std::string &replaceWith)
{
	char        currChar;
	char        nextChar;
	std::string currentWord;
	std::string output;

	output.reserve( str.length() * 2 );

	for(size_t i=0; i<str.length(); i++) {
		// Look ahead
		if( str.length() > i + 1 ) {
			nextChar = str[i+1];
		} else {
			// we are at the end of buffer
			nextChar = '\0';
		}

		currChar = str[i];
		if(!IsWordCharA( currChar, currentWord.length() )) {
			output += str[i];
			currentWord.clear();

		} else {

			currentWord += currChar;
			if(IsWordCharA(nextChar, currentWord.length())) {
				// do nothing

			} else if( !IsWordCharA(nextChar, currentWord.length()) && currentWord == word ) {
				output += replaceWith;
				currentWord.clear();

			} else {
				output += currentWord;
				currentWord.clear();
			}

		}
	}
	return output;
}

// Helper string find metho
wxString ReplaceWord(const wxString &str, const wxString &word, const wxString &replaceWith)
{
	wxString currChar;
	wxString nextChar;
	wxString currentWord;
	wxString output;
	for(size_t i=0; i<str.Length(); i++) {
		// Look ahead
		if( str.Length() > i + 1 ) {
			nextChar = str[i+1];
		} else {
			// we are at the end of buffer
			nextChar = wxT('\0');
		}

		currChar = str[i];
		if(!IsWordChar( currChar, currentWord.Length() )) {
			output << str[i];
			currentWord.Clear();

		} else {

			currentWord << currChar;
			if(IsWordChar(nextChar, currentWord.Length())) {
				// do nothing

			} else if( !IsWordChar(nextChar, currentWord.Length()) && currentWord == word ) {
				output << replaceWith;
				currentWord.Clear();

			} else {
				output << currentWord;
				currentWord.Clear();
			}

		}
	}
	return output;
}

wxArrayString TokenizeWords(const wxString &str)
{
	wxString currChar;
	wxString nextChar;
	wxString currentWord;
	wxArrayString outputArr;
	
	wxString::const_iterator iter = str.begin();
	for(; iter != str.end(); iter++) {
		// Look ahead
		if( (iter + 1) != str.end() ) {
			 nextChar = *(iter+1);
		} else {
			// we are at the end of buffer
			nextChar = wxT('\0');
		}

		currChar = *iter;
		if(!IsWordChar( currChar, currentWord.Length() )) {
			currentWord.Clear();

		} else {

			currentWord << currChar;
			if(IsWordChar(nextChar, currentWord.Length())) {
				// do nothing

			} else {

				outputArr.Add(currentWord);
				currentWord.Clear();
			}

		}
	}
	return outputArr;
}

static PPTable* ms_instance = NULL;
	
void PPToken::processArgs(const wxString &argsList)
{
	args = wxStringTokenize(argsList, wxT(","), wxTOKEN_STRTOK);

	// replace all occurances of 'arg' with %1, %2 etc
	for(size_t i=0; i<args.GetCount(); i++) {
		wxString replaceWith = wxString::Format(wxT("%%%d"), (int)i);
#if wxVERSION_NUMBER < 2900
		replacement = ReplaceWord(replacement, args.Item(i), replaceWith);
#else
		std::string res = ReplaceWordA(replacement.To8BitData().data(), args.Item(i).To8BitData().data(), replaceWith.To8BitData().data());
		if(res.empty()) {
			replacement.clear();
			
		} else {
			replacement = wxString::From8BitData(res.c_str());
			
		}
#endif
	}
}

void PPToken::print(wxFFile &fp)
{
#if 0
	wxString buff;
	buff << wxT("Name          : ") << name << wxT("\n");
	buff << wxT("replacement   : ") << replacement << wxT("\n");
	buff << wxT("isFunctionLike: ") << isFunctionLike << wxT("\n");
	if(isFunctionLike) {
		for(size_t i=0; i<args.size(); i++) {
			buff << wxT("Arg: ") << args.Item(i) << wxT("\n");
		}
	}
	buff << wxT(" ---- \n");
	fp.Write(buff);
#else
	wxString buff;
	buff << name << wxT("(") << (flags & IsFunctionLike) << wxT(")") << wxT("=") << replacement << wxT("\n");
	fp.Write(buff);
#endif
}

wxString PPToken::fullname() const
{
	wxString fullname;
	fullname << name;
	if(flags & IsFunctionLike) {
		fullname << wxT("(");
		for(size_t i=0; i<args.size(); i++) {
			fullname << wxT("%") << i << wxT(",");
		}
		if(args.size()) {
			fullname.RemoveLast();
		}
		fullname << wxT(")");
	}
	return fullname;
}

void PPToken::squeeze()
{
	std::set<wxString> alreadyReplacedMacros;

	// perform the squeeze 5 times max
	for(size_t count=0; count < 5; count++) {
		bool modified(false);

		// get list of possible macros in the replacement
		wxArrayString tmpWords = TokenizeWords(replacement);
		wxArrayString words;

		// make sure that a word is not been replaced more than once
		// this will avoid recursion
		// an example (taken from qglobal.h of the Qt library):
		//
		// #define qDebug QT_NO_QDEBUG_MACRO
		// #define QT_NO_QDEBUG_MACRO if(1); else qDebug
		//
		for(size_t i=0; i<tmpWords.size(); i++) {
			if(alreadyReplacedMacros.find(tmpWords.Item(i)) == alreadyReplacedMacros.end()){
				alreadyReplacedMacros.insert(tmpWords[i]);
				words.Add(tmpWords[i]);
			}
		}

		for(size_t i=0; i<words.size(); i++) {
			PPToken tok = PPTable::Instance()->Token(words.Item(i));
			if(tok.flags & IsValid) {
				if(tok.flags & IsFunctionLike) {
					int where = replacement.Find(words.Item(i));
					if(where != wxNOT_FOUND) {
						wxString      initList;
						wxArrayString initListArr;
						if(readInitList( replacement, where + words.Item(i).Length(), initList, initListArr )) {
							tok.expandOnce(initListArr);

							replacement.Remove(where, words.Item(i).Length() + initList.Length());
							tok.replacement.Replace(wxT("##"), wxT(""));
							replacement.insert(where, tok.replacement);
							modified = true;
						}
					}

				} else {
					if(replacement.Replace(words.Item(i), tok.replacement)) {
						modified = true;
					}
				}
			}
		}

		if(!modified)
			break;
	}
	replacement.Replace(wxT("##"), wxT(""));
}

bool PPToken::readInitList(const std::string& in, size_t from, std::string& initList, std::vector<std::string>& initListArr)
{
	if(in.length() < from) {
		return false;
	}

	std::string tmpString = in.substr(from);
	size_t      start     = tmpString.find('(');
	if(start == std::string::npos ) {
		return false;
	}

	// skip the open brace
	tmpString = tmpString.substr(start+1);

	for(size_t i=0; i<start; i++) {
		initList += " ";
	}

	initList += "(";
	std::string word;
	int depth(1);

	for(size_t i=0; i<tmpString.length(); i++) {
		char ch = tmpString[i];
		initList += ch;
		switch(ch) {
		case ')':
			depth --;
			if(depth == 0) {
				initListArr.push_back(word);
				return true;
			} else {
				word += ch;
			}
			break;
		case '(':
			depth++;
			word += ch;
			break;
		case ',':
			if(depth == 1) {
				initListArr.push_back(word);
				word.clear();
			} else {
				word += ch;
			}
			break;
		default:
			word += ch;
			break;
		}
	}
	return false;
}

bool PPToken::readInitList(const wxString &in, int from, wxString& initList, wxArrayString& initListArr)
{
	if((int)in.Length() < from) {
		return false;
	}

	wxString tmpString = in.Mid(from);
	int start = tmpString.Find(wxT("("));
	if(start == wxNOT_FOUND ) {
		return false;
	}
	tmpString = tmpString.Mid(start+1);

	for(size_t i=0; i<(size_t)start; i++) {
		initList << wxT(" ");
	}

	initList << wxT("(");
	wxString word;
	int depth(1);

	for(size_t i=0; i<tmpString.Length(); i++) {
		wxChar ch = tmpString[i];
		initList << ch;
		switch(ch) {
		case wxT(')'):
			depth --;
			if(depth == 0) {
				initListArr.Add(word);
				return true;
			} else {
				word << ch;
			}
			break;
		case wxT('('):
			depth++;
			word << ch;
			break;
		case wxT(','):
			if(depth == 1) {
				initListArr.Add(word);
				word.Clear();
			} else {
				word << ch;
			}
			break;
		default:
			word << ch;
			break;
		}
	}
	return false;
}

void PPToken::expandOnce(const wxArrayString& initList)
{
	if(initList.size() != args.size())
		return;

	for(size_t i=0; i<args.size(); i++) {
		wxString placeHolder;
		placeHolder << wxT("%") << i;
		
		wxString replaceWith = initList.Item(i);
		replaceWith.Trim().Trim(false);
		
		if(replaceWith.Contains(placeHolder))
			continue;
		
		replacement.Replace(placeHolder, initList.Item(i));
	}
}

wxString PPToken::signature() const
{
	wxString sig;
	if(flags & IsFunctionLike) {
		sig << wxT("(");
		for(size_t i=0; i<args.size(); i++) {
			sig << wxT("%") << i << wxT(",");
		}
		if(args.size()) {
			sig.RemoveLast();
		}
		sig << wxT(")");
	}
	return sig;
}

///////////////////////////////////////////////////

PPTable::PPTable()
{
}

PPTable::~PPTable()
{
}

PPTable* PPTable::Instance()
{
	if(ms_instance == NULL) {
		ms_instance = new PPTable();
	}
	return ms_instance;
}

void PPTable::Release()
{
	if(ms_instance) {
		delete ms_instance;
	}
	ms_instance = NULL;
}

PPToken PPTable::Token(const wxString& name)
{
	std::map<wxString, PPToken>::iterator iter = m_table.find(name);
	if(iter == m_table.end()) {
		return PPToken();
	}

	return iter->second;
}

void PPTable::Add(const PPToken& token)
{
	if(token.name.IsEmpty())
		return;

	wxString name = token.name;
	name.Trim().Trim(false);
	std::map<wxString, PPToken>::iterator iter = m_table.find(name);
	if(iter == m_table.end())
		m_table[name] = token;
	else {
		// if the new token's replacement is empty and the current one is NOT empty,
		// replace the two (we prefer empty replacements)
		if(iter->second.flags & PPToken::IsOverridable && !iter->second.replacement.IsEmpty() && token.replacement.IsEmpty()) {
			m_table[name] = token;
		}
	}
}

void PPTable::AddUsed(const wxString& name)
{
	if(name.IsEmpty()) {
		return;
	}
	m_namesUsed.insert(name);
}

void PPTable::Print(wxFFile &fp)
{
	std::map<wxString, PPToken>::iterator iter = m_table.begin();
	for(; iter != m_table.end(); iter++) {
		iter->second.print(fp);
	}
}

bool PPTable::Contains(const wxString& name)
{
	std::map<wxString, PPToken>::iterator iter = m_table.find(name);
	return iter != m_table.end();
}

wxString PPTable::Export()
{
	wxString table;
	std::map<wxString, PPToken>::iterator iter = m_table.begin();
	for(; iter != m_table.end(); iter++) {
		iter->second.squeeze();
		wxString replacement = iter->second.replacement;
		replacement.Trim().Trim(false);
		
		// remove extra whitespaces
		while(replacement.Replace(wxT("  "), wxT(" "))){}
		
		if(replacement.IsEmpty()) {
			table << iter->second.fullname() << wxT("\n");

		} else if(iter->second.flags & PPToken::IsFunctionLike) {
			table << iter->second.fullname() << wxT("=") << replacement << wxT("\n");

		} else {
			// macros with replacement but they are not in a form of a function
			// we take only macros that thier replacement is not a number
			long v(-1);
			if(!replacement.ToLong(&v) && !replacement.ToLong(&v, 8) && !replacement.ToLong(&v, 16) && replacement.find(wxT('"')) == wxString::npos && !replacement.StartsWith(wxT("0x"))) {
				table << iter->second.fullname() << wxT("=") << replacement << wxT("\n");
			}
		}
	}
	return table;
}

void PPTable::Squeeze()
{
	std::map<wxString, PPToken>::iterator iter = m_table.begin();
	for(; iter != m_table.end(); iter++) {
		m_table[iter->first].squeeze();
	}
}

void PPTable::Clear()
{
	m_table.clear();
}

void PPTable::ClearNamesUsed()
{
	m_namesUsed.clear();
}

bool CLReplacePattern(const wxString& in, const wxString& pattern, const wxString& replaceWith, wxString &outStr)
{
	int where = pattern.Find(wxT("%0"));
	if(where != wxNOT_FOUND) {
		wxString replacement(replaceWith);

		// a patterened expression
		wxString searchFor = pattern.BeforeFirst(wxT('('));
		where = in.Find(searchFor);
		if(where == wxNOT_FOUND) {
			return false;
		}

		wxString      initList;
		wxArrayString initListArr;
		if(PPToken::readInitList(in, searchFor.Length() + where, initList, initListArr) == false)
			return false;

		outStr = in;
		// update the 'replacement' with the actual values ( replace %0..%n)
		for(size_t i=0; i<initListArr.size(); i++) {
			wxString placeHolder;
			placeHolder << wxT("%") << i;
			replacement.Replace(placeHolder, initListArr.Item(i));
		}

		outStr.Remove(where, searchFor.Length() + initList.Length());
		outStr.insert(where, replacement);
		return true;

	} else {
		if(in.Find(pattern) == wxNOT_FOUND) {
			return false;
		}
		// simple replacement
		outStr = ReplaceWord(in, pattern, replaceWith);
		return outStr != in;
	}
}

std::string replacement;

bool CLReplacePatternA(const std::string& in, const CLReplacement& repl, std::string& outStr)
{
	if(repl.is_compound) {
		size_t where = in.find(repl.searchFor);
		if(where == std::string::npos)
			return false;

		std::string              initList;
		std::vector<std::string> initListArr;
		if(PPToken::readInitList(in, repl.searchFor.length() + where, initList, initListArr) == false)
			return false;

		// update the 'replacement' with the actual values ( replace %0..%n)
		replacement = repl.replaceWith;
		char placeHolder[4];
		for(size_t i=0; i<initListArr.size(); i++) {

            memset(placeHolder, 0, sizeof(placeHolder));
            sprintf(placeHolder, "%%%d", (int)i);

			size_t pos = replacement.find(placeHolder);
			const std::string& init = initListArr[i];
            while( pos != std::string::npos ) {
				replacement.replace(pos, strlen(placeHolder), init.c_str());

				// search for the next match
                pos = replacement.find(placeHolder, pos + 1);
            }
		}

		outStr = in;
		where = outStr.find(repl.searchFor);
		if(where == std::string::npos)
			return false;

		outStr.replace(where, repl.searchFor.length() + initList.length(), replacement);
		return true;

	} else {

		size_t where = in.find(repl.searchFor);
		if(where == std::string::npos) {
			return false;
		}

		outStr = ReplaceWordA(in, repl.searchFor, repl.replaceWith);

//		outStr = in;
//		outStr.replace(where, repl.searchFor.length(), repl.replaceWith);

		// simple replacement
		return outStr != in;
	}
}

void CLReplacement::construct(const std::string& pattern, const std::string& replacement)
{
	is_ok = true;
	full_pattern = pattern;
	is_compound  = full_pattern.find("%0") != std::string::npos;
	if(is_compound) {
		// a patterened expression
		replaceWith = replacement;
		size_t where = pattern.find('(');
		if(where == std::string::npos) {
			is_ok = false;
			return;
		}

		searchFor = pattern.substr(0, where);
		if(searchFor.empty()){
			is_ok = false;
			return;
		}

	} else {
		// simple Key=Value pair
		replaceWith = replacement;
		searchFor   = full_pattern;
	}
}

