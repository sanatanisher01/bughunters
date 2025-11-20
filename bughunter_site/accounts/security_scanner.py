import re
import json

class SecurityScanner:
    """Scanner for detecting exposed credentials and sensitive information"""
    
    # Patterns for detecting various types of credentials
    CREDENTIAL_PATTERNS = {
        'api_keys': [
            r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?',
            r'(?i)(secret[_-]?key|secretkey)\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?',
            r'(?i)(access[_-]?key|accesskey)\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?',
        ],
        'passwords': [
            r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?([^\s"\']{6,})["\']?',
            r'(?i)(db[_-]?password|database[_-]?password)\s*[:=]\s*["\']?([^\s"\']{6,})["\']?',
        ],
        'smtp_credentials': [
            r'(?i)(smtp[_-]?password|email[_-]?password)\s*[:=]\s*["\']?([^\s"\']{6,})["\']?',
            r'(?i)(smtp[_-]?user|email[_-]?user)\s*[:=]\s*["\']?([^\s"\'@]+@[^\s"\']+)["\']?',
            r'(?i)(smtp[_-]?host|email[_-]?host)\s*[:=]\s*["\']?([^\s"\']+\.[^\s"\']+)["\']?',
        ],
        'cloud_services': [
            r'(?i)(aws[_-]?access[_-]?key|amazon[_-]?key)\s*[:=]\s*["\']?([A-Z0-9]{20})["\']?',
            r'(?i)(aws[_-]?secret[_-]?key)\s*[:=]\s*["\']?([A-Za-z0-9/+=]{40})["\']?',
            r'(?i)(cloudinary[_-]?url|cloudinary[_-]?api)\s*[:=]\s*["\']?([^\s"\']{20,})["\']?',
            r'(?i)(firebase[_-]?key|google[_-]?api[_-]?key)\s*[:=]\s*["\']?([A-Za-z0-9_-]{20,})["\']?',
        ],
        'database_urls': [
            r'(?i)(database[_-]?url|db[_-]?url)\s*[:=]\s*["\']?(postgresql://[^\s"\']+)["\']?',
            r'(?i)(mongodb[_-]?uri|mongo[_-]?url)\s*[:=]\s*["\']?(mongodb://[^\s"\']+)["\']?',
            r'(?i)(redis[_-]?url)\s*[:=]\s*["\']?(redis://[^\s"\']+)["\']?',
        ],
        'jwt_tokens': [
            r'(?i)(jwt[_-]?secret|token[_-]?secret)\s*[:=]\s*["\']?([A-Za-z0-9_-]{20,})["\']?',
            r'(?i)(bearer[_-]?token)\s*[:=]\s*["\']?([A-Za-z0-9._-]{20,})["\']?',
        ],
        'private_keys': [
            r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
            r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----',
            r'(?i)(private[_-]?key)\s*[:=]\s*["\']?([A-Za-z0-9/+=\n\r-]{100,})["\']?',
        ]
    }
    
    # File extensions to scan
    SCANNABLE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.php', 
        '.cs', '.cpp', '.c', '.rs', '.kt', '.scala', '.sh', '.bash', '.env',
        '.config', '.json', '.yaml', '.yml', '.xml', '.properties', '.ini'
    }
    
    @staticmethod
    def scan_content(content, file_path):
        """Scan file content for exposed credentials"""
        findings = []
        
        for category, patterns in SecurityScanner.CREDENTIAL_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.MULTILINE)
                
                for match in matches:
                    line_number = content[:match.start()].count('\n') + 1
                    
                    # Get the matched credential (usually group 2)
                    credential = match.group(2) if len(match.groups()) >= 2 else match.group(0)
                    
                    # Skip common placeholder values
                    if SecurityScanner._is_placeholder(credential):
                        continue
                    
                    finding = {
                        'type': 'security_vulnerability',
                        'category': 'exposed_credentials',
                        'subcategory': category,
                        'severity': 'critical',
                        'line': line_number,
                        'message': f'Exposed {category.replace("_", " ").title()}: {credential[:20]}...',
                        'description': f'Potential {category.replace("_", " ")} found in code. This could be a security risk if the code is shared publicly.',
                        'code_snippet': SecurityScanner._get_code_snippet(content, line_number),
                        'recommendation': SecurityScanner._get_recommendation(category),
                        'credential_preview': credential[:10] + '...' if len(credential) > 10 else credential
                    }
                    
                    findings.append(finding)
        
        return findings
    
    @staticmethod
    def _is_placeholder(credential):
        """Check if the credential is likely a placeholder"""
        placeholders = [
            'your-api-key', 'your-secret-key', 'your-password', 'example',
            'placeholder', 'changeme', 'password123', 'secret123', 'test',
            'localhost', '127.0.0.1', 'username', 'user', 'admin', 'root'
        ]
        
        credential_lower = credential.lower()
        return any(placeholder in credential_lower for placeholder in placeholders)
    
    @staticmethod
    def _get_code_snippet(content, line_number, context_lines=2):
        """Get code snippet around the line with credential"""
        lines = content.split('\n')
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        snippet_lines = []
        for i in range(start, end):
            prefix = ">>> " if i == line_number - 1 else "    "
            snippet_lines.append(f"{prefix}{i+1}: {lines[i]}")
        
        return '\n'.join(snippet_lines)
    
    @staticmethod
    def _get_recommendation(category):
        """Get security recommendation for the credential type"""
        recommendations = {
            'api_keys': 'Move API keys to environment variables or secure configuration files. Use .env files and add them to .gitignore.',
            'passwords': 'Never hardcode passwords. Use environment variables, secure vaults, or configuration management systems.',
            'smtp_credentials': 'Store SMTP credentials in environment variables. Use app-specific passwords for email services.',
            'cloud_services': 'Use IAM roles, service accounts, or environment variables for cloud service authentication.',
            'database_urls': 'Store database connection strings in environment variables or secure configuration.',
            'jwt_tokens': 'Generate JWT secrets dynamically and store them securely. Never commit tokens to version control.',
            'private_keys': 'Private keys should never be in source code. Use secure key management systems.'
        }
        
        return recommendations.get(category, 'Store sensitive information in environment variables or secure configuration systems.')
    
    @staticmethod
    def scan_project_files(code_files):
        """Scan all project files for security issues"""
        security_findings = []
        
        for file_info in code_files:
            file_path = file_info['path']
            content = file_info['content']
            
            # Check if file should be scanned
            file_ext = '.' + file_path.split('.')[-1].lower() if '.' in file_path else ''
            if file_ext not in SecurityScanner.SCANNABLE_EXTENSIONS:
                continue
            
            # Scan file content
            findings = SecurityScanner.scan_content(content, file_path)
            
            for finding in findings:
                finding['file'] = file_path
                security_findings.append(finding)
        
        return security_findings