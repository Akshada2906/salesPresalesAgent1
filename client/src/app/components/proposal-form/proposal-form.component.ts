// import { Component, inject } from "@angular/core";
// import {
//   FormBuilder,
//   FormGroup,
//   FormsModule,
//   ReactiveFormsModule,
//   Validators,
// } from "@angular/forms";
// import { HttpClient, HttpClientModule } from "@angular/common/http";
// import { HttpErrorResponse } from "@angular/common/http";
// import { Observable } from "rxjs";
// import { CommonModule } from "@angular/common";
// import { MatIconModule } from "@angular/material/icon";
// import { MarkdownModule } from "ngx-markdown";
// import { MarkdownToHtmlModule } from "../../markdown-to-html.module";
// import { HttpRequestsConstants } from "../../services/http-requests-constants";

// interface ProposalData {
//   customer: string;
//   title: string;
//   requirements: string;
// }

// interface ProposalSection {
//   title: string;
//   content: string;
//   layout_rank: number;
// }

// interface GeneratedProposal {
//   proposal: {
//     [key: string]: ProposalSection;
//   };
// }

// @Component({
//   selector: "app-proposal-form",
//   standalone: true,
//   imports: [
//     FormsModule,
//     CommonModule,
//     ReactiveFormsModule,
//     HttpClientModule,
//     MatIconModule,
//     MarkdownModule,
//     MarkdownToHtmlModule,
//   ],
//   templateUrl: "./proposal-form.component.html",
//   styleUrls: ["./proposal-form.component.css"],
//   providers: [HttpClient],
// })
// export class ProposalFormComponent {
//   proposalForm: FormGroup;
//   isLoading = false;
//   proposal: ProposalSection[] = [];
//   isEditing = false;

//   private http = inject(HttpClient);
//   private fb = inject(FormBuilder);

//   constructor() {
//     this.proposalForm = this.fb.group({
//       customer: ["", Validators.required],
//       title: ["", Validators.required],
//       requirements: ["", Validators.required],
//     });
//   }

//   generateProposal(data: ProposalData): Observable<GeneratedProposal> {
//     return this.http.post<GeneratedProposal>(
//       HttpRequestsConstants.GENERATE_PROPOSAL,
//       data
//     );
//   }

//   handleSubmit(): void {
//     if (this.proposalForm.invalid) {
//       return;
//     }

//     this.isLoading = true;

//     this.generateProposal(this.proposalForm.value).subscribe(
//       (result) => {
//         const proposalSections = Object.values(result.proposal);
//         proposalSections.sort((a, b) => a.layout_rank - b.layout_rank);
//         this.proposal = proposalSections;
//         this.isLoading = false;
//       },
//       (error: HttpErrorResponse) => {
//         console.error("Error generating proposal:", error);
//         this.isLoading = false;
//       }
//     );
//   }

//   toggleEdit(): void {
//     this.isEditing = !this.isEditing;
//   }

//   downloadProposal(): void {
//     const content = this.proposal
//       .map(section => `# ${section.title}\n\n${section.content}`)
//       .join('\n\n');
    
//     const blob = new Blob([content], { 
//       type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
//     });
//     const url = URL.createObjectURL(blob);
//     const a = document.createElement('a');
//     a.href = url;
//     a.download = 'proposal.docx';
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//     URL.revokeObjectURL(url);
//   }

//   get f() {
//     return this.proposalForm.controls;
//   }
// }

import { Component, inject } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { HttpClient, HttpClientModule } from "@angular/common/http";
import { HttpErrorResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { CommonModule } from "@angular/common";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import { MarkdownModule } from "ngx-markdown";
import { MarkdownToHtmlModule } from "../../markdown-to-html.module";
import { HttpRequestsConstants } from "../../services/http-requests-constants";

interface ProposalData {
  customer: string;
  title: string;
  requirements: string;
  completion: string;
  amount: string;
}

interface ProposalSection {
  title: string;
  content: string;
  layout_rank: number;
}

interface GeneratedProposal {
  proposal: {
    [key: string]: ProposalSection;
  };
}

interface ProgressState {
  percentage: number;
  message: string;
}

@Component({
  selector: "app-proposal-form",
  templateUrl: "./proposal-form.component.html",
  styleUrls: ["./proposal-form.component.css"],
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatIconModule,
    MatProgressBarModule,
    MarkdownModule,
    MarkdownToHtmlModule,
  ],
  providers: [HttpClient],
})
export class ProposalFormComponent {
  proposalForm: FormGroup;
  isLoading = false;
  proposal: ProposalSection[] = [];
  isEditing = false;
  progress: ProgressState = {
    percentage: 0,
    message: '',
  };

  private http = inject(HttpClient);
  private fb = inject(FormBuilder);

  private progressStates: ProgressState[] = [
    { percentage: 25, message: 'Analyzing requirements and project scope...' },
    { percentage: 50, message: 'Generating proposal structure and outline...' },
    { percentage: 75, message: 'Searching relevant case studies from database...' },
    { percentage: 90, message: 'Formatting and organizing proposal sections...' },
    { percentage: 100, message: 'Finalizing your proposal...' }
  ];

  constructor() {
    this.proposalForm = this.fb.group({
      customer: ["", Validators.required],
      title: ["", Validators.required],
      requirements: ["", Validators.required],
      completion: ["", Validators.required],
      amount: ["", Validators.required],
    });
  }

  generateProposal(data: ProposalData): Observable<GeneratedProposal> {
    return this.http.post<GeneratedProposal>(
      HttpRequestsConstants.GENERATE_PROPOSAL,
      data
    );
  }

  private simulateProgress(): void {
    let currentIndex = 0;
    
    const progressInterval = setInterval(() => {
      if (currentIndex < this.progressStates.length) {
        this.progress = this.progressStates[currentIndex];
        currentIndex++;
      } else {
        clearInterval(progressInterval);
      }
    }, 4000); 
  }

  handleSubmit(): void {
    if (this.proposalForm.invalid) {
      Object.keys(this.proposalForm.controls).forEach(key => {
        const control = this.proposalForm.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    this.isLoading = true;
    this.progress = { percentage: 0, message: 'Initiating proposal generation...' };
    this.simulateProgress();

    this.generateProposal(this.proposalForm.value).subscribe({
      next: (result) => {
        const proposalSections = Object.values(result.proposal);
        proposalSections.sort((a, b) => a.layout_rank - b.layout_rank);
        this.proposal = proposalSections;
        this.isLoading = false;
        this.progress = { percentage: 0, message: '' };
      },
      error: (error: HttpErrorResponse) => {
        console.error("Error generating proposal:", error);
        this.isLoading = false;
        this.progress = { percentage: 0, message: '' };
      }
    });
  }

  toggleEdit(): void {
    this.isEditing = !this.isEditing;
  }

  downloadProposal(): void {
    const content = this.proposal
      .map(section => `# ${section.title}\n\n${section.content}`)
      .join('\n\n');
   
    const blob = new Blob([content], {
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `proposal-${this.proposalForm.get('title')?.value || 'untitled'}.docx`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  get formControls() {
    return this.proposalForm.controls;
  }

  getErrorMessage(controlName: string): string {
    const control = this.proposalForm.get(controlName);
    if (control?.hasError('required')) {
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} is required`;
    }
    return '';
  }
}