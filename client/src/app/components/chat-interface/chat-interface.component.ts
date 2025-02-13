import {
  Component,
  OnInit,
  SecurityContext,
  ViewChild,
  ElementRef,
  AfterViewChecked,
} from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { FormsModule } from "@angular/forms";
import { CommonModule } from "@angular/common";
import { ChatSidebarComponent } from "../chat-sidebar/chat-sidebar.component";
import { ChatMessageComponent } from "../chat-message/chat-message.component";
import { MatIconModule } from "@angular/material/icon";
import { DomSanitizer } from "@angular/platform-browser";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { HttpRequestsConstants } from "../../services/http-requests-constants";

interface Message {
  text: string;
  isBot: boolean;
  timestamp: string;
  taskInfo?: {
    techStack?: {
      name: string;
      description: string;
      usage: string;
    }[];
  };
}

@Component({
  selector: "app-chat-interface",
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    ChatSidebarComponent,
    ChatMessageComponent,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: "./chat-interface.component.html",
  styleUrls: ["./chat-interface.component.css"],
})
export class ChatInterfaceComponent implements OnInit, AfterViewChecked {
  botMessage: any = [];
  messages: Message[] = [
    {
      text: "Hello! I'm your sales assistant. How can I help you today?",
      isBot: true,
      timestamp: new Date().toLocaleTimeString(),
      taskInfo: {
        techStack: [],
      },
    },
  ];
  input: string = "";
  isSidebarOpen: boolean = true;
  isLoading: boolean = false;
  private previousMessageLength: number = 0;

  @ViewChild("chatMessagesContainer")
  private chatMessagesContainer!: ElementRef;

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  ngOnInit(): void {}

  ngAfterViewChecked(): void {
    if (this.messages.length > this.previousMessageLength) {
      this.scrollToBottom();
      this.previousMessageLength = this.messages.length;
    }
  }

  private scrollToBottom(): void {
    try {
      this.chatMessagesContainer.nativeElement.scrollTop =
        this.chatMessagesContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }

  async callChatAPI(query: string) {
    try {
      const response = await this.http
        .post<any>(HttpRequestsConstants.CHAT_AGENT, { query })
        .toPromise();
      return response;
    } catch (error) {
      console.error("Error calling chat API:", error);
      return {
        answer: "I'm sorry, I encountered an error processing your request.",
      };
    }
  }

  async handleSend() {
    if (!this.input.trim()) return;

    this.isLoading = true;

    const newMessage: Message = {
      text: this.input,
      isBot: false,
      timestamp: new Date().toLocaleTimeString(),
    };

    this.messages.push(newMessage);
    this.input = "";

    const botAnswer = await this.callChatAPI(newMessage.text);

    const botResponse: Message = {
      text: botAnswer.message,
      isBot: true,
      timestamp: new Date().toLocaleTimeString(),
      taskInfo: {
        techStack: botAnswer.techs,
      },
    };

    if (botAnswer.companies_list) {
      const formattedList = this.formatCompaniesList(botAnswer.companies_list);
      botResponse.text += formattedList;
    }

    this.isLoading = false;

    this.messages.push(botResponse);
  }

  formatCompaniesList(companiesList: any[]) {
    let formattedList = "";

    companiesList.forEach((company, index) => {
      formattedList += `
<div class="company-case-study${index > 0 ? " mt-4" : ""}">
<p><strong>Client:</strong> ${
        this.sanitizer.sanitize(SecurityContext.HTML, company["Client"]) || ""
      }</p>
<p><strong>Business Challenge:</strong> ${
        this.sanitizer.sanitize(
          SecurityContext.HTML,
          company["Business Challenge"]
        ) || ""
      }</p>
 <p><strong>Our Solution:</strong> ${
   this.sanitizer.sanitize(SecurityContext.HTML, company["Our Solution"]) || ""
 }</p>
<p><strong>Technologies Used:</strong> ${
        this.sanitizer.sanitize(
          SecurityContext.HTML,
          company["Technologies Used"]
        ) || ""
      }</p>
      </div> `;
    });

    return formattedList;
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  get currentTaskInfo() {
    return this.messages[this.messages.length - 1]?.taskInfo;
  }
}
